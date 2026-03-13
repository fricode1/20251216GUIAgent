# 个人猜测

python脚本。如果真是的话，那就万事大吉了。

如果不是代码形式的话，还能是什么呢？目前想不出第二种可能。

# 研究代码

开源： https://github.com/iflytek/astron-rpa/

https://github.com/iflytek/astron-rpa/?tab=readme-ov-file：
- astronverse.actionlib：原子操作定义和执行

https://github.com/iflytek/astron-rpa/blob/main/engine/components/astronverse-cua/src/astronverse/cua/computer_use.py
- GUI Agent 智能体

# 可视化设计器对应 JSON 流程定义

by comate：
```json
{
  "metadata": {
    "name": "InvoiceProcessing",
    "version": "1.0"
  },
  "nodes": [
    {
      "id": "n1",
      "type": "browser.open",
      "params": {"url": "https://example.com"}
    },
    {
      "id": "n2",
      "type": "excel.read",
      "deps": ["n1"],
      "params": {"path": "/tmp/data.xlsx"}
    }
  ]
}
```

# 自动化脚本的内部调用和外部调用

从RPA软件内部固然可以调用自动化脚本。但是是否支持外部调用？

by comate：支持MCP和REST API调用。

# 如何用MCP调用一个自动化脚本？

需要 RPA 服务器地址。应该是部署了容器后就能获得

# 部署星辰RPA的服务端和客户端

astron-rpa\BUILD_GUIDE.zh.md

## 容器部署星辰RPA（后端）

关键：http://localhost:8000/ 用户名：admin 密码：123（comate帮我找到的）

## 部署星辰RPA前端

```powershell
cd C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\code\astron-rpa

./build.bat -p "C:\Users\admin\Documents\GitHub\fri\20251216GUIAgent\code\astron-rpa\astron_py313\Scripts\python.exe"
```
