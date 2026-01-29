# 交通违章监控系统 - 前端

基于 React + Vite + Ant Design 的交通违章监控系统前端应用。

## 功能特性

- ✅ 创建违章监控应用
- ✅ 应用列表查询（支持分页）
- ✅ 删除应用
- ✅ 查看抓拍图片（支持分页）
- ✅ 实时状态展示

## 快速开始

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

前端将运行在 `http://localhost:3000`

### 构建生产版本

```bash
npm run build
```

## 技术栈

- React 18
- Vite 5
- Ant Design 5
- Axios
- Day.js

## 项目结构

```
frontend/
├── src/
│   ├── api/
│   │   └── index.js          # API 接口封装
│   ├── App.jsx               # 主应用组件
│   └── main.jsx              # 应用入口
├── index.html                # HTML 模板
├── vite.config.js            # Vite 配置
└── package.json              # 项目配置
```

## 注意事项

1. 确保后端服务运行在 `http://localhost:8000`
2. 前端通过 Vite 代理转发 `/violation` 请求到后端
3. 图片预览功能需要 MinIO 服务正常运行
