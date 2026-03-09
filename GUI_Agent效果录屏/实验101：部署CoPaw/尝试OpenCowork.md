# 选择理由

https://mp.weixin.qq.com/s/NylUAZLAWiBdkf6bkqbgOQ

专门提出支持GUI Operation。

# 安装方式

windows是安装 exe。

需要配置大模型：测试连通成功。
- Base Url = https://qianfan.baidubce.com/v2
- model = deepseek-v3.1-250821
- bce-v3/ALTAK-1FEA4o5wnpQo04XofR8lD/0c6a65aa9ac05d5597fafc8d27d30f1341efe22d

运行报错：Error: Cannot read properties of undefined (reading 'push')

可能原因：openai协议不行，得改成 anthropic 协议
- b2cbf2e6e78c46b2a6e13b44a8cd9887.1tbiu9JwkNp9rpX7
- model: glm-5
- base url: https://open.bigmodel.cn/api/anthropic

改完后，报错：Error: request ended without sending any events

采用 glm-4.7 成功。

# 踩坑历程

- 问题：安装新版本后无法启动
- 重装后，通过双击快捷方式启动。

- 问题：点击开始没有反应