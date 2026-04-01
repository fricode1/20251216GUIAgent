import requests
import config

import urllib3
# 禁用 requests 在使用 verify=False 时产生的安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_deploy_tasks():
    """列出所有布控应用"""
    return_str = ''
    base_url = "https://62.168.243.10:19080"
    url = f"{base_url}/mrag/api/deploy/tasks/list"
    headers = {
        "Authorization": config.authorization
    }
    # 发送 GET 请求
    response = requests.get(url, headers=headers, verify=False)
    try:
        response.raise_for_status()
        result = response.json()

        if result:
            # 判断业务状态码 code 是否为 0 (通常 0 代表成功)
            if result.get("code") == 0:
                data = result.get("data", {})
                total = data.get("total", 0)
                task_list = data.get("list", [])

                # 遍历并打印精简后的任务列表信息，方便查看
                for task in task_list:
                    task_id = task.get('id', 'N/A')
                    task_name = task.get('name', 'N/A')
                    status_code = task.get('status', 0)
                    status_str = "运行中" if status_code == 1 else "已停止"
                    return_str += '任务ID：{}，任务状态：{}，任务名称：{}。\n'.format(task_id, status_str, task_name)
            else:
                return_str += f"❌ 获取失败，服务器返回信息: {result.get('msg')}"
    except Exception as e:
        return_str += e
    return  return_str


if __name__ == "__main__":
    print(list_deploy_tasks())