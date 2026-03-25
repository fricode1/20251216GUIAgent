---
name: deploy_task_manager
description: "Manage video surveillance deployment tasks (视频布控应用). Use this skill when the user wants to create, list, start a deploy task, or view the deployment alarm results. It interacts with the backend REST APIs."
metadata:
  {
    "copaw":
      {
        "emoji": "🚨",
        "requires": {}
      }
  }
---
# 布控任务管理工具箱 (Deploy Task Manager)

Use this skill when the user asks to interact with video surveillance deployment tasks (布控应用/布控任务). This includes listing existing tasks, creating new tasks, starting a specific task, and checking the alarm/trigger results of a task.

## Authentication (Required)

**ALL** API requests must include the following HTTP header:
`Authorization: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiLljZfpmLPmtYvor5UiLCJsb2dpbl91c2VyX2tleSI6ImM4OGI2M2IzLTlmZTEtNDVlNi1hMWZmLWRlY2MxYjk4ZTBiNyJ9.Q9zjaNHmr_gsTwPzJqYnekYwkUwHJQZmQiBG6fI53UEQtu6XLiCT4gOxpWPGXVq2LH1iiFO6w6DrAd3fs1NzqA`

*Note: Use `execute_shell_command` with `curl` or a dedicated HTTP request tool to make these API calls.*

## Supported Actions & API Mapping

### 1. 列出所有布控应用 (List Deploy Tasks)
- **Condition**: User asks to see all tasks, or you need to find a Task ID based on a Task Name.
- **Endpoint**: `GET https://62.168.243.10:19080/mrag/api/deploy/tasks/list`
- **Action**: Fetch the list and summarize it for the user. Display the `id`, `name`, `desc`, and `status` of the tasks.

### 2. 创建布控应用 (Create Deploy Task)
- **Condition**: User asks to create a new deployment/monitoring task.
- **Endpoint**: `POST https://62.168.243.10:19080/mrag/api/deploy/tasks/create`
- **Action**: You must construct a JSON body. If the user hasn't provided the necessary information, politely ask them for:
  - `name`: 任务名称 (Task Name)
  - `text`: 监控目标的简短文本 (e.g., "穿白衣服的人")
  - `prompt`: 详细的大模型判定提示词 (e.g., "如果图中人员符合描述返回Y...")
  - `space_time_list`: 关联的设备ID和时间段 (device_id, start_time, end_time)
  *Default values you can use if not specified*: `target_type: "person"`, `deploy_type: 0`, `distance: 0.8`.

### 3. 启动布控应用 (Start Deploy Task)
- **Condition**: User asks to start/enable a specific task.
- **Endpoint**: `POST https://62.168.243.10:19080/mrag/api/deploy/tasks/start`
- **Workflow**:
  1. If the user provides a task *name* instead of an *ID*, first call the **List** API to find the corresponding `id`.
  2. Send the request with the JSON body: `{"id": "THE_TASK_ID"}`.
  3. Inform the user whether the start command was successful.

### 4. 查看布控结果 (View Alarm Results)
- **Condition**: User wants to see the results, alarms, or matched images of a task.
- **Endpoint**: `GET https://62.168.243.10:19080/mrag/api/deploy/alarm/list?id={task_id}&pageNo=1&pageSize=10`
- **Workflow**:
  1. Get the task `id` (use the List API if the user only provides a name).
  2. Fetch the results.
  3. Extract and present the data nicely to the user: Show the `time`, `similar` (similarity score), and format the `url` as a Markdown image `![alarm_image](url)`.

## Workflow Examples

- **User**: "帮我启动一下'渣土车'的布控任务。"
  **AI Action**: 
  1. Call GET `/tasks/list`.
  2. Parse JSON, find the task named "渣土车" (id: "21").
  3. Call POST `/tasks/start` with `{"id": "21"}`.
  4. Reply: "渣土车布控任务（ID:21）已成功启动。"

- **User**: "查看一下打架斗殴的报警结果。"
  **AI Action**:
  1. Call GET `/tasks/list`, find ID for "打架斗殴" (id: "45").
  2. Call GET `/alarm/list?id=45&pageNo=1&pageSize=10`.
  3. Reply with a summarized list of recent alarms and display the image URLs.

## Safety and Behavior

- Always verify the Task ID before starting a task or querying alarms.
- Do not expose the raw Authorization Token to the user in the chat interface.
- If the API returns a non-zero `code` or an error message, translate it into user-friendly language and explain what went wrong.
- For image creation (e.g., `image_base64`), if the user cannot provide it, leave it as an empty string `""` or `[]` as supported by the API.