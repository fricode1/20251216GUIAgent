---
name: query_train_ticket
description: "当用户希望查询火车票信息（如车次、票价等）时使用此技能。明确要求先生成 Python 脚本并保存为文件（如 query_ticket.py），然后通过 shell 运行该文件来调用指定的 RPA 工作流 API，传入出发地、到达地和出发时间，获取列车信息。适用于一切需要代查火车票的场景。"
metadata:
  {
    "copaw":
      {
        "emoji": "🚄",
        "requires": {}
      }
  }
---

# 火车票查询（RPA API）参考

当用户需要**查询火车票**、**寻找列车车次**或**了解某两地之间的火车票情况**时，应使用本 skill。该技能通过**编写 Python 脚本文件并执行**的方式来触发后台 RPA（机器人流程自动化）工作流，从而自动查询并返回结果。

## 何时使用

- 用户说：「帮我查一下明天从福州到北京的火车票」
- 用户说：「2026年3月28日去北京的高铁有哪些？」
- 用户需要获取指定日期、指定出发地和目的地的列车信息。

*注意：如果用户没有提供完整的“出发地”、“到达地”和“出发时间”，请先向用户询问补齐这些信息，再生成代码进行查询。*

## 使用方式（写入文件后执行）

严禁直接在 shell 中使用 `python -c "..."` 这种单行命令执行。请务必遵循以下两个步骤：

### 步骤 1：将代码写入 Python 文件
请根据用户的需求，将出发地、到达地、出发时间动态替换到以下代码中，并将这段代码保存为一个独立的文件，例如命名为 `query_ticket.py`。

```python
# 文件名: query_ticket.py
import requests

url = "http://172.20.118.153:32742/api/rpa-openapi/workflows/execute"
headers = {
    "Authorization": "Bearer 931bba7rX73k15oAsJR8KkfXiSZBwhG0",
    "Content-Type": "application/json"
}

# 请根据用户的需求，动态替换 params 中的参数值
data = {
    "project_id": "2034832313526808576",
    "params": {
        "input_variable": "<出发地，例如：福州>", 
        "to_station": "<到达地，例如：北京>", 
        "start_date": "<出发时间，格式为 YYYY-MM-DD，例如：2026-03-28>"
    }
}

response = requests.post(url, headers=headers, json=data, timeout=30)
print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")