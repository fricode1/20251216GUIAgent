调用 http://172.20.118.153:32742/api/rpa-openapi/workflows/execute

headers:

Authorization = Bearer 931bba7rX73k15oAsJR8KkfXiSZBwhG0

body:
```json
{
    "project_id": "2034832313526808576",
    "params": {
        "input_variable": "福州",
        "to_station": "北京",
        "start_date": "2026-03-28"
    }
}
```
其中，出发地、到达地和出发时间可以指定。

# 响应

## 情况1

```json
{
    "code": "0000",
    "msg": "",
    "data": {
        "execution": {
            "id": "e12169af-7675-4ee6-a7c5-63cf91998591",
            "project_id": "2034832313526808576",
            "status": "FAILED",
            "parameters": {
                "input_variable": "福州",
                "to_station": "北京",
                "start_date": "2026-03-28"
            },
            "result": null,
            "error": "send uuid empty",
            "exec_position": "EXECUTOR",
            "version": 12,
            "user_id": "21d6400d-a1cd-4bea-9dfa-c40605039525",
            "start_time": "2026-03-23T02:51:09",
            "end_time": "2026-03-23T02:51:09"
        }
    }
}
```

说明没有启动 rpa 客户端

## 情况2

```json
{
    "code": "0000",
    "msg": "",
    "data": {
        "execution": {
            "id": "ef52a647-0ae4-41d6-a327-3cfdc0672924",
            "project_id": "2034832313526808576",
            "status": "COMPLETED",
            "parameters": {
                "input_variable": "福州",
                "to_station": "北京",
                "start_date": "2026-03-28"
            },
            "result": {
                "code": "0000",
                "msg": "运行成功",
                "data": {
                    "input_variable": "福州",
                    "to_station": "北京",
                    "start_date": "2026-03-28",
                    "output_variable": "G964智复静查看票价"
                }
            },
            "error": null,
            "exec_position": "EXECUTOR",
            "version": 12,
            "user_id": "21d6400d-a1cd-4bea-9dfa-c40605039525",
            "start_time": "2026-03-23T02:52:09",
            "end_time": "2026-03-23T02:52:28"
        }
    }
}
```

正常返回结果为："output_variable": "G964智复静查看票价"

# AI 调用

我想让AI智能调用上述内容，需要写 ai skill 吗？

## skill 模板

```text
---
name: browser_visible
description: "当用户希望打开真实可见的浏览器窗口（而非后台无头模式）时，使用 browser_use 的 headed 参数启动浏览器，随后可正常 open/snapshot/click 等。适用于用户想亲眼看到页面、演示或调试场景。"
metadata:
  {
    "copaw":
      {
        "emoji": "🖥️",
        "requires": {}
      }
  }
---

# 可见浏览器（真实窗口）参考

默认情况下，**browser_use** 在后台以无头（headless）模式运行，不会弹出浏览器窗口。当用户明确希望**打开真正的浏览器窗口**、**看到浏览器界面**、**有界面的浏览器**或**可见浏览器**时，应使用本 skill：先以 **headed** 模式启动浏览器，再按需打开页面并操作。

## 何时使用

- 用户说：「打开真实浏览器」「打开有界面的浏览器」「我想看到浏览器」「不要后台，要能看到窗口」
- 用户希望亲眼看到页面加载、点击、填表等过程（演示、调试、教学）
- 用户需要与可见页面交互（如登录、验证码等需人工参与的场景）

## 使用方式（browser_use）

1. **先以可见模式启动浏览器**  
   调用 **browser_use**，`action` 为 `start`，并传入 **headed=true**：
   ```json
   {"action": "start", "headed": true}
   ```
   成功后会出现一个真实的 Chromium 浏览器窗口。

2. **再按需打开页面并操作**  
   与无头模式用法相同，例如：
   - 打开 URL：`{"action": "open", "url": "https://example.com"}`
   - 获取页面结构：`{"action": "snapshot"}`
   - 点击、输入等：使用 `ref` 或 `selector` 进行 click、type 等

3. **关闭可见浏览器**  
   使用完毕后可调用：`{"action": "stop"}` 关闭浏览器。

## 与默认（无头）模式的区别

| 模式     | 启动方式                    | 是否弹出窗口 |
|----------|-----------------------------|--------------|
| 无头模式 | `{"action": "start"}`       | 否（后台）   |
| 可见模式 | `{"action": "start", "headed": true}` | 是（真实窗口） |

## 注意

- 若当前已有浏览器在运行，需要先 `stop` 再以 `headed: true` 重新 `start`，才能切换到可见窗口。
- 可见模式会占用桌面并需要图形环境，服务器或无图形环境可能无法使用。
```

## gemini 3.1 pro 生成的结果

```markdown
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
```