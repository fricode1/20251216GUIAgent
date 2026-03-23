---
name: query_train_ticket
description: "当用户希望查询火车票信息（如车次、票价等）时使用此技能。通过调用指定的 RPA 工作流 API，传入出发地、到达地和出发时间，获取列车信息。适用于一切需要代查火车票的场景。"
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

当用户需要**查询火车票**、**寻找列车车次**或**了解某两地之间的火车票情况**时，应使用本 skill。该技能通过触发后台 RPA（机器人流程自动化）工作流来自动查询并返回结果。

## 何时使用

- 用户说：「帮我查一下明天从福州到北京的火车票」
- 用户说：「2026年3月28日去北京的高铁有哪些？」
- 用户需要获取指定日期、指定出发地和目的地的列车信息。

*注意：如果用户没有提供完整的“出发地”、“到达地”和“出发时间”，请先向用户询问补齐这些信息，再调用本接口。*

## 使用方式（HTTP 调用）

通过发送 HTTP POST 请求调用 RPA 接口执行查询。

- **请求地址**: `POST http://172.20.118.153:32742/api/rpa-openapi/workflows/execute`
- **请求头 (Headers)**:
  ```http
  Authorization: Bearer 931bba7rX73k15oAsJR8KkfXiSZBwhG0
  Content-Type: application/json
  ```
- **请求体 (Body)**:
  ```json
  {
      "project_id": "2034832313526808576",
      "params": {
          "input_variable": "<出发地，例如：福州>",
          "to_station": "<到达地，例如：北京>",
          "start_date": "<出发时间，格式为 YYYY-MM-DD，例如：2026-03-28>"
      }
  }
  ```

## 响应处理与结果解析

调用接口后，需根据返回的 JSON 数据判断执行状态并向用户反馈：

### 情况1：查询成功
当 `data.execution.status` 为 `"COMPLETED"` 时，表示 RPA 查询成功。
- **解析路径**：提取 `data.execution.result.data.output_variable` 的值。
- **示例数据**：`"output_variable": "G964智复静查看票价"`
- **反馈用户**：将提取到的车次和票务信息自然地播报给用户（例如：“为您查到相关车次信息：G964...”）。

### 情况2：RPA 客户端未启动 (失败)
当 `data.execution.status` 为 `"FAILED"`，且 `data.execution.error` 包含 `"send uuid empty"` 时，表示后台运行环境异常。
- **反馈用户**：告知用户：“当前 RPA 客户端未启动，请先检查并启动 RPA 客户端后再试。”

## 注意

1. **日期格式**：`start_date` 必须转换为 `YYYY-MM-DD` 格式。如果用户说“明天”，请根据当前日期计算出准确的日期字符串后再调用。
2. **固定参数**：`project_id` 是固定的 `"2034832313526808576"`，不可更改。
3. 接口调用可能需要一定时间（RPA执行通常需要十几秒到几十秒），在实际调用前可提示用户“正在为您启动后台查询，请稍候...”。