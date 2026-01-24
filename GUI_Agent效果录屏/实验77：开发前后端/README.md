# 行人交通违法查询平台

基于 Vue3 + FastAPI + SQLite + MinIO 的行人交通违法查询系统

## 系统架构

- **前端**: Vue 3 + Vite
- **后端**: Python FastAPI
- **数据库**: SQLite
- **对象存储**: MinIO
- **LLM**: OpenAI API (可选，支持正则表达式回退)

## 功能特点

1. 智能解析用户问题中的地点和时间信息
2. 流式返回违章图像
3. 图像存储到 MinIO
4. 违章记录保存到 SQLite 数据库
5. 实时在前端展示查询结果

## 安装部署

### 前置要求

- Python 3.8+
- Node.js 16+
- MinIO 服务

### 1. 安装 MinIO

#### Windows (PowerShell)
```powershell
# 下载 MinIO
Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "minio.exe"

# 启动 MinIO
.\minio.exe server C:\minio-data --console-address ":9001"
```

#### Linux/Mac
```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server /minio-data --console-address ":9001"
```

默认访问地址:
- API: http://localhost:9000
- Console: http://localhost:9001
- 默认账号: minioadmin / minioadmin

### 2. 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
# 创建 .env 文件
cat > .env << EOF
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
OPENAI_API_KEY=your_openai_api_key_here
EOF

# 启动服务
python main.py
```

后端将在 http://localhost:8000 运行

### 3. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 运行

## 使用说明

1. 打开浏览器访问 http://localhost:3000
2. 在输入框中输入查询问题，例如：
   - `查询新华路昨天的行人违章`
   - `查询中山路今天的违章情况`
3. 点击发送按钮
4. 系统会实时展示查询到的违章图像和详细信息

## API 接口

### POST /api/query
查询违章记录（流式响应）

**请求体:**
```json
{
  "question": "查询新华路昨天的行人违章"
}
```

**响应:** Server-Sent Events (SSE) 流式数据

### GET /api/violations
获取所有违章记录

**响应:**
```json
[
  {
    "id": 1,
    "minio_path": "traffic-violations/violation_xxx.jpg",
    "time": "20240115",
    "location": "新华路",
    "name": "张三",
    "id_number": "370982199001011234",
    "created_at": "2024-01-15 10:30:00"
  }
]
```

### GET /health
健康检查

## 项目结构

```
.
├── backend/
│   ├── main.py          # FastAPI 主程序
│   ├── requirements.txt # Python 依赖
│   └── .env             # 环境变量配置
├── frontend/
│   ├── src/
│   │   ├── App.vue      # 主应用组件
│   │   └── main.js      # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 技术实现

### 后端实现
- 使用 FastAPI 构建 RESTful API
- 使用 LLM 解析地点和时间（支持正则表达式回退）
- 使用 MinIO 存储图像文件
- 使用 SQLite 存储违章记录
- 使用 SSE (Server-Sent Events) 实现流式响应

### 前端实现
- 使用 Vue 3 Composition API
- 使用 Axios 处理 HTTP 请求和 SSE 流
- 响应式 UI 设计
- 实时图像展示

## 注意事项

1. 确保 MinIO 服务正常运行
2. 如需使用 LLM 解析，需配置 OPENAI_API_KEY
3. 默认使用正则表达式解析，不需要 API Key
4. 图像 URL 为示例 URL，实际使用时需替换为真实数据源
