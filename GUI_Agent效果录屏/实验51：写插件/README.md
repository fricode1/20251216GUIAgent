# Dummy Chat - Chrome浏览器插件

这是一个带对话功能的Chrome浏览器扩展，实现了Echo Bot（回显机器人）功能。

## 功能特点

- 💬 **对话界面**: 美观的聊天UI，类似微信/Telegram的聊天体验
- 🔄 **Echo回复**: 发送什么消息，Bot就回复什么消息
- 📱 **侧边栏集成**: 使用Chrome Side Panel API，不干扰主页面
- ✨ **动画效果**: 消息淡入动画，流畅的用户体验

## 文件说明

- `manifest.json` - 扩展配置文件（Manifest V3）
- `sidebar.html` - 侧边栏页面结构和样式
- `sidebar.js` - 对话逻辑处理
- `background.js` - 后台脚本

## 安装方法

1. 打开Chrome浏览器
2. 在地址栏输入 `chrome://extensions/`
3. 打开右上角的"开发者模式"开关
4. 点击"加载已解压的扩展程序"
5. 选择本插件所在文件夹

## 使用方法

1. 安装扩展后，点击浏览器工具栏的扩展图标
2. 侧边栏会打开，显示对话界面
3. 在输入框中输入消息
4. 点击"发送"按钮或按回车键
5. Bot会在0.5秒后回复相同的内容

## 快捷操作

- **Enter键**: 发送消息
- **自动聚焦**: 页面加载后自动聚焦输入框
- **按钮状态**: 输入框为空时发送按钮禁用

## 技术要点

1. **Manifest V3**: 使用最新的Chrome扩展配置格式
2. **sidePanel API**: 使用Chrome 114+版本的侧边栏API
3. **纯前端实现**: 无需后端服务器，所有逻辑在浏览器端完成
4. **DOM操作**: 使用原生JavaScript处理消息添加和滚动
5. **CSS动画**: 消息淡入效果和悬停交互

## 浏览器要求

- Chrome 版本 114 或更高（支持Side Panel API）
- 或其他基于Chromium的浏览器（Edge、Brave等）的相应版本

## 扩展建议

可以将此Echo Bot改造成：
- 🤖 接入真实的AI聊天API（如OpenAI、Claude等）
- 💾 保存聊天历史到localStorage
- 🎨 支持多主题切换
- 📎 支持发送图片和文件
- 🔍 对话历史搜索功能

## 自定义

如需修改Bot的回复逻辑，编辑`sidebar.js`文件中的`sendMessage()`函数。
