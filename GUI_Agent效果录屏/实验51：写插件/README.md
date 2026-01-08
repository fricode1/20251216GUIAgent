# HelloWorld Sidebar - Chrome浏览器插件

这是一个简单的Chrome浏览器扩展，在侧边栏显示"helloworld"。

## 文件说明

- `manifest.json` - 扩展配置文件（Manifest V3）
- `sidebar.html` - 侧边栏页面
- `background.js` - 后台脚本

## 安装方法

1. 打开Chrome浏览器
2. 在地址栏输入 `chrome://extensions/`
3. 打开右上角的"开发者模式"开关
4. 点击"加载已解压的扩展程序"
5. 选择本插件所在文件夹

## 使用方法

### 方法一：通过侧边栏
1. 安装扩展后，点击浏览器工具栏的扩展图标
2. 侧边栏会自动打开，显示"helloworld"

### 方法二：通过右键菜单
1. 在浏览器任意页面上右键点击
2. 选择"在侧边栏中打开"

### 方法三：固定到工具栏
1. 点击浏览器右上角的拼图图标（扩展程序）
2. 找到"HelloWorld Sidebar"
3. 点击图钉图标，将其固定到工具栏
4. 之后点击工具栏图标即可打开侧边栏

## 技术要点

1. **Manifest V3**: 使用最新的Chrome扩展配置格式
2. **sidePanel API**: 使用Chrome 114+版本的侧边栏API
3. **权限**: 仅需要`sidePanel`权限
4. **Service Worker**: 使用后台服务工作者（替代旧的background页面）

## 浏览器要求

- Chrome 版本 114 或更高（支持Side Panel API）
- 或其他基于Chromium的浏览器（Edge、Brave等）的相应版本

## 自定义

如需修改显示内容，编辑`sidebar.html`文件中的`.message`部分。
