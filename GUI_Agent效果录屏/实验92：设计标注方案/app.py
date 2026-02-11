from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import base64
from DrissionPage import ChromiumPage
import io
from openai import OpenAI
from uitls import simplify_dom

app = Flask(__name__)

# 数据存储路径
DATA_FILE = 'annotations.json'

# 大模型配置
client = OpenAI(
    api_key="sk-K2h63uJJNVPjkox2uEESH5NlM8Ub9gg8rh6TuesgbgQpy6k5",
    base_url="https://api.moonshot.cn/v1"
)
MODEL_NAME = "kimi-k2.5"

# 初始化 DrissionPage (单例模式)
_page = None

def get_page():
    global _page
    if _page is None:
        _page = ChromiumPage()
        # 初始加载目标页面
        file_path = os.path.abspath('target_page.html')
        _page.get(f'file://{file_path}')
    return _page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screenshot')
def screenshot():
    """获取目标网页的截图"""
    page = get_page()
    img_bytes = page.get_screenshot(as_bytes=True)
    return send_file(io.BytesIO(img_bytes), mimetype='image/png')

@app.route('/dom')
def get_dom():
    """获取目标网页的 DOM HTML"""
    page = get_page()
    return jsonify({'html': page.html})

@app.route('/goto', methods=['POST'])
def goto():
    """跳转到指定 URL"""
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': '未提供 URL'})
    
    page = get_page()
    try:
        page.get(url)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    """接收指令和 DOM，调用 LLM 生成代码"""
    print('开始调用大模型')
    data = request.json
    instruction = data.get('instruction')
    dom_html = data.get('dom_html')
    dom_html = simplify_dom(dom_html)
    print(dom_html)
    
    prompt = f"""你是一个网页操作助手。请根据提供的网页 DOM HTML 和自然语言指令，生成执行该操作的 DrissionPage 代码。
要求：
1. 只输出 Python 代码，不要有任何解释。
2. 假设已经存在一个名为 `page` 的 DrissionPage 对象。
3. 代码应该简洁、准确。
4. 如果要填写文本框，需要先清除原有内容，再输入新内容。
5. 如果要填写文本框，要先将待填写的内容放入剪贴板，然后使用 `tab.actions.type((Keys.CTRL_A, Keys.CTRL_V))` 方法。
6. 如果要点击元素，使用 `tab.ele(element_selector).click()` 方法。
7. 对于唯一性元素，尽量通过文本内容匹配。如果文本重复，请绑定最近的唯一父容器。

网页 DOM HTML:
{dom_html}

自然语言指令:
{instruction}
"""

    try:
        print('正在调用大模型...')
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个专业的 DrissionPage 自动化专家。"},
                {"role": "user", "content": prompt}
            ]
        )
        print('大模型调用完成')
        llm_output = response.choices[0].message.content.strip()
        print(llm_output)
        # 移除 Markdown 代码块标记（如果有）
        if llm_output.startswith("```python"):
            llm_output = llm_output.split("```python")[1].split("```")[0].strip()
        elif llm_output.startswith("```"):
            llm_output = llm_output.split("```")[1].split("```")[0].strip()
            
        return jsonify({
            'llm_output': llm_output
        })
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': f"调用大模型失败: {str(e)}"})

@app.route('/execute', methods=['POST'])
def execute():
    """在目标网页上执行代码"""
    data = request.json
    code = data.get('code')
    page = get_page()
    
    try:
        # 在后端执行 DrissionPage 代码
        # 为了安全和上下文，我们将 page 对象暴露给 exec 环境
        exec_globals = {'page': page}
        exec(code, exec_globals)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/save', methods=['POST'])
def save():
    """保存标注数据，包含 DOM HTML"""
    data = request.json
    
    annotations = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                annotations = json.load(f)
            except json.JSONDecodeError:
                annotations = []
    
    annotations.append({
        'dom_html': data.get('dom_html'),
        'instruction': data.get('instruction'),
        'correct_code': data.get('correct_code'),
        'timestamp': data.get('timestamp')
    })
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(annotations, f, ensure_ascii=False, indent=4)
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=False, port=5000) # 生产环境下关闭 debug 以避免重复初始化浏览器
