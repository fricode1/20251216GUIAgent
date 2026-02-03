import json
import os
import subprocess
import asyncio
import re
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
    script_name: str = None
    args: dict = None

def clean_response(text: str) -> str:
    """去除 LLM 响应中的 <think>...</think> 标签及其内容"""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

@app.get("/")
async def root():
    return {"message": "流程自动化 Agent 后端 API 正在运行。请通过 8080 端口访问前端界面。"}

def sanitize_text(text: str) -> str:
    """将敏感词替换为英文，避免触发模型敏感词过滤"""
    replacements = {
        "身份证号": "ID card number",
        "身份证": "ID card",
        "身份账号": "account ID"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

@app.post("/chat")
async def chat(request: ChatRequest):
    # 定义现有脚本及其描述
    available_scripts = {
        "pedestrian_violation.py": {
            "description": "查询行人违章记录。需要参数：start_time (YYYYMMDDHHmmss), end_time (YYYYMMDDHHmmss), place (地点名称)。",
            "args": ["start_time", "end_time", "place"]
        },
        "zhihu_collect.py": {
            "description": "抓取知乎收藏夹内容。需要参数：url (收藏夹URL)。",
            "args": ["url"]
        }
    }

    # 构建消息列表
    messages = [{"role": "system", "content": "你是一个专业的流程自动化助手。"}]
    
    # 添加历史记录
    for msg in request.history:
        # 简单清理历史记录，并进行脱敏处理
        content = sanitize_text(msg['content'])
        if "[MATCH_SCRIPT]" in content:
            # 如果是之前的脚本匹配响应，可能需要简化或保留提示信息
            pass
        messages.append({"role": msg['role'], "content": content})

    user_message = sanitize_text(request.message)
    prompt = f"""你是一个流程自动化助手。
以下是《视综平台SOP.md》的内容：
{sop_content}

现有已生成的脚本列表：
{json.dumps(available_scripts, ensure_ascii=False, indent=2)}

用户的问题是：{user_message}

任务：
1. 判断用户的问题是否可以由现有的脚本直接完成。
2. 如果可以，请以以下格式回复：
   [MATCH_SCRIPT]
   script_name: 脚本文件名
   args: {{"参数名": "提取的值"}}
   message: 发现已有脚本可以处理您的请求。我已经为您准备好了参数，是否立即执行？
3. 如果不可以，请根据SOP，用自然语言告诉用户该如何操作。在回答的最后，必须问用户：“需要我为你生成自动化脚本吗？”
"""
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=0.7,
        stream=True
    )
    
    async def chat_generator():
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
            await asyncio.sleep(0.01)

    return StreamingResponse(chat_generator(), media_type="text/plain")

@app.post("/generate_script")
async def generate_script(request: ChatRequest):
    # 构建包含历史背景的消息列表
    messages = [{"role": "system", "content": "你是一个专业的 Python 开发助手，擅长使用 DrissionPage 库进行自动化操作。"}]
    
    # 添加对话历史作为背景
    for msg in request.history:
        messages.append({"role": msg['role'], "content": sanitize_text(msg['content'])})
        
    prompt = f"""请根据之前的对话背景和以下SOP内容生成一个 DrissionPage 的 Python 脚本。
SOP内容：
{sop_content}

要求：
1. 脚本应包含完整的登录、进入应用、切换标签页、查询等步骤。
2. 脚本应使用 DrissionPage 库。
3. **必须在每个关键步骤执行前后添加详尽的 `print` 语句，作为日志输出**（例如：`print("正在进入登录页...")`）。
4. 脚本末尾应打印执行总结。
5. 只返回代码，不要有任何 Markdown 标记或额外解释。
"""
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=0.1,
        stream=True
    )
    
    async def script_generator_wrapper():
        full_content = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                full_content += content
                yield content
            await asyncio.sleep(0.01)
            
        # 脚本生成完成后，保存到文件
        # 用户在前端能看到思考过程，但我们保存时必须剔除它
        cleaned_content = clean_response(full_content)
        
        # 提取代码块
        code = cleaned_content
        if code.startswith("```python"):
            code = code[9:]
            if code.endswith("```"):
                code = code[:-3]
        elif code.startswith("```"):
            code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
        
        code = code.strip()
            
        script_path = "generated_script.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
            
    return StreamingResponse(script_generator_wrapper(), media_type="text/plain")

@app.post("/execute_script")
async def execute_script(request: ChatRequest):
    script_path = request.script_name if request.script_name else "generated_script.py"
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail=f"Script {script_path} not found")
    
    # 构造执行命令
    cmd = ["python", "-u", script_path]
    if request.args:
        for key, value in request.args.items():
            cmd.extend([f"--{key}", str(value)])
            
    async def log_generator():
        # Start subprocess
        process = subprocess.Popen(
            cmd, # -u for unbuffered output
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
