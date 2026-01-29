import json
import os
import subprocess
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

client = OpenAI(
    api_key=config['api_key'],
    base_url=config['api_base']
)

# Load SOP
with open('视综平台SOP.md', 'r', encoding='utf-8') as f:
    sop_content = f.read()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
async def root():
    return {"message": "流程自动化 Agent 后端 API 正在运行。请通过 8080 端口访问前端界面。"}

@app.post("/chat")
async def chat(request: ChatRequest):
    prompt = f"""你是一个流程自动化助手。
以下是《视综平台SOP.md》的内容：
{sop_content}

用户的问题是：{request.message}

请根据SOP，用自然语言告诉用户该如何操作。
在回答的最后，必须问用户：“需要我为你生成自动化脚本吗？”
"""
    
    response = client.chat.completions.create(
        model=config['model'],
        messages=[{"role": "system", "content": "你是一个专业的流程自动化助手。"}, {"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return {"reply": response.choices[0].message.content}

@app.post("/generate_script")
async def generate_script(request: ChatRequest):
    # Extract name from message if possible, or default
    # For simplicity, we assume the user is asking about a specific person
    prompt = f"""请根据以下SOP内容生成一个 DrissionPage 的 Python 脚本。
SOP内容：
{sop_content}

要求：
1. 脚本应包含完整的登录、进入应用、切换标签页、查询等步骤。
2. 脚本应使用 DrissionPage 库。
3. 脚本应将姓名作为变量 `person_name`，默认值为 '张三丰'。
4. **必须在每个关键步骤执行前后添加详尽的 `print` 语句，作为日志输出**（例如：`print("正在进入登录页...")`）。
5. 脚本末尾应打印执行总结。
6. 只返回代码，不要有任何 Markdown 标记或额外解释。
"""
    
    response = client.chat.completions.create(
        model=config['model'],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    code = response.choices[0].message.content.strip()
    if code.startswith("```python"):
        code = code[9:-3]
    elif code.startswith("```"):
        code = code[3:-3]
        
    script_path = "generated_script.py"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
        
    return {"reply": "脚本已生成。需要我为你执行该脚本文件吗？", "script_path": script_path}

@app.post("/execute_script")
async def execute_script(request: ChatRequest):
    script_path = "generated_script.py"
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Script not found")
    
    async def log_generator():
        # Start subprocess
        process = subprocess.Popen(
            ["python", "-u", script_path], # -u for unbuffered output
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        yield "开始执行脚本...\n"
        
        # Read output line by line
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                yield f"> {line}"
            await asyncio.sleep(0.1) # Small delay to be gentle on CPU
            
        return_code = process.poll()
        yield f"\n脚本执行完成，退出代码: {return_code}\n"

    return StreamingResponse(log_generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
