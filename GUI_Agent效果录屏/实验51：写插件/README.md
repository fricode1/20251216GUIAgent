# AI Chat - DeepSeek Chrome插件

这是一个集成DeepSeek大模型的AI聊天Chrome浏览器扩展，在侧边栏提供智能对话功能。

## 功能特点

- 💬 **AI对话**: 接入DeepSeek大模型，支持自然语言对话
- 🧠 **上下文记忆**: 自动保存对话历史，支持多轮对话
- 📱 **侧边栏集成**: 使用Chrome Side Panel API，不干扰主页面浏览
- ✨ **流畅体验**: 实时"正在思考..."提示，消息淡入动画
- ⚡ **快速响应**: 直接调用API，无需中转服务器

## 文件说明

- `manifest.json` - 扩展配置文件（Manifest V3）
- `sidebar.html` - 侧边栏页面结构和样式
- `sidebar.js` - 对话逻辑和API调用
- `background.js` - 后台脚本

## 安装方法

1. 打开Chrome浏览器
2. 在地址栏输入 `chrome://extensions/`
3. 打开右上角的"开发者模式"开关
4. 点击"加载已解压的扩展程序"
5. 选择本插件所在文件夹

## 使用方法

1. 安装扩展后，点击浏览器工具栏的扩展图标
2. 侧边栏会打开，显示"AI助手已就绪"
3. 在输入框中输入问题或消息
4. 点击"发送"按钮或按回车键
5. AI会思考后给出智能回复

## API配置

当前使用的DeepSeek API配置（在`sidebar.js`中）：

```javascript
const API_CONFIG = {
  baseURL: 'https://api.deepseek.com',
  apiKey: 'sk-6fda4f18a54140c6ae408fdd13cfe97d',
  model: 'deepseek-chat'
};
```

如需更换API密钥或模型，修改上述配置即可。

## 快捷操作

- **Enter键**: 发送消息
- **自动聚焦**: 页面加载后自动聚焦输入框
- **按钮状态**: 输入框为空时发送按钮禁用
- **思考提示**: 调用API时显示"🤔 正在思考..."

## 技术要点

1. **Manifest V3**: 使用最新的Chrome扩展配置格式
2. **sidePanel API**: 使用Chrome 114+版本的侧边栏API
3. **DeepSeek API**: OpenAI兼容的API接口
4. **异步处理**: 使用async/await处理API请求
5. **对话历史**: 自动维护上下文，支持多轮对话
6. **错误处理**: 完善的API错误捕获和提示

## 浏览器要求

- Chrome 版本 114 或更高（支持Side Panel API）
- 或其他基于Chromium的浏览器（Edge、Brave等）的相应版本

## 安全提示

⚠️ **注意**: 当前实现中API密钥直接硬编码在前端代码中。在生产环境中，建议：
- 使用后端服务器代理API请求
- 或使用Chrome Storage API加密存储密钥
- 不要在公开的代码中暴露API密钥

## 改进建议

可以扩展的功能：
- 💾 保存聊天历史到localStorage
- 🎨 支持多主题切换
- 📎 支持发送图片和文件
- 🔍 对话历史搜索功能
- 🌐 支持其他AI模型（OpenAI、Claude等）
- ⚙️ 设置页面，让用户自定义API配置
- 📊 Token使用统计
- 🌙 Markdown渲染支持

## 自定义

如需修改AI模型或参数，编辑`sidebar.js`文件：
- **API配置**: 修改`API_CONFIG`对象
- **模型参数**: 修改`callDeepSeekAPI()`函数中的`temperature`和`max_tokens`
- **系统提示词**: 在messages数组中添加system角色消息
