import threading
import time
from flask import Flask, jsonify

app = Flask(__name__)

# ================= 纯内存状态 =================
x_logs = []       # 业务逻辑产生的全部内容容器
cursor = 0        # 记录外界上次读取到了哪里

# ================= 函数 B：负责输出增量内容 =================
@app.route('/get_incremental', methods=['GET'])
def function_b():
    """
    当 CoPaw 通过 HTTP 请求这个接口时触发。
    返回从游标开始的新内容，并更新游标。
    """
    global x_logs, cursor
    
    # 获取增量内容
    new_content = x_logs[cursor:]
    
    # 【核心】：更新游标
    cursor = len(x_logs)
    
    # 返回给 CoPaw（以 JSON 格式，大模型最容易解析）
    return jsonify({
        "count": len(new_content),
        "new_logs": new_content
    })

def start_http_server():
    """启动轻量级 HTTP 服务"""
    # 禁用 Flask 默认的启动提示音和日志，保持终端干净
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    
    # 在 5050 端口启动，提供内部接口
    app.run(host='127.0.0.1', port=5050, debug=False, use_reloader=False)

# ================= 函数 A：业务逻辑 =================
def function_a():
    """
    你的核心业务逻辑。持续运行，不断向 x_logs 追加内容。
    """
    global x_logs
    print("业务逻辑开始持续运行，并在 5050 端口提供 CoPaw 接口...")
    
    count = 0
    while True:
        time.sleep(3) # 模拟业务耗时
        count += 1
        
        # 业务产生了一条新信息，直接存入内存
        new_msg = f"处理完成：第 {count} 批次数据"
        x_logs.append(new_msg)
        
        # 可选：如果担心程序跑几个月内存溢出，可以加一个简单的清理逻辑
        # 比如：当 cursor 和 len(x_logs) 都很大时，清空前面已经读取过的数据

if __name__ == '__main__':
    # 1. 开一个后台线程，运行 HTTP 接口 (也就是挂载了函数B)
    api_thread = threading.Thread(target=start_http_server, daemon=True)
    api_thread.start()
    
    # 2. 主线程运行持续的业务逻辑 (函数A)
    function_a()

"""
# 每天早上 9 点，或者每两小时执行一次
copaw cron create --type agent --name "Python业务增量汇报" --cron "*/1 * * * *" --channel console --target-user "你的用户ID" --target-session "会话ID" --text "请通过 HTTP GET 请求 http://127.0.0.1:5050/get_incremental 获取最新业务数据。如果返回的 count 为 0，告诉我'暂无新进展'；如果有新内容，请帮我总结这些 new_logs，并发送给我。"
"""