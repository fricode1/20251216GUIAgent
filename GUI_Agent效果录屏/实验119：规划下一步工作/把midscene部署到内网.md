# 在互联网安装所需要的命令

npm install -g @midscene/cli
npm install -g @midscene/web
npm install -g tsx

# 再没有互联网的环境中无法执行 npm install 怎么办

（npm pack: 无法解决依赖问题）

在有网电脑上：创建一个空文件夹 offline-packages。在里面运行 npm init -y。将你需要的所有包安装进去：

```bash
npm install tsx @midscene/cli @midscene/web  # 列出你需要的所有包
```

注意，有网电脑要与无网电脑操作系统相同。

此时，你的 node_modules 里已经有了这些包及其所有递归依赖。

打包迁移：直接把这个 node_modules 文件夹压缩（.zip 或 .tar.gz）。拷贝到内网目标项目的根目录下。在内网解压后执行：

```bash
npm install --offline
```

注：npm install --offline 会尝试从本地的 node_modules 中链接依赖，而不去请求网络。

验证安装是否成功：

```bash
npx midscene
```

# 安装浏览器插件

在有网电脑上下载插件压缩包：https://github.com/web-infra-dev/midscene/releases

将压缩包拷贝到内网并解压，定位到包含 manifest.json 的那一层目录

在chrome中进入chrome://extensions/ 点击 “加载已解压的扩展程序” (Load unpacked)。

选择刚才的文件夹