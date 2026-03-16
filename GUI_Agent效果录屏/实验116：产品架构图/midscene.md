# 桥接模式

```powershell
npm install @midscene/web tsx --save-dev
$env:MIDSCENE_MODEL_BASE_URL="https://api.z.ai/api/paas/v4"
$env:MIDSCENE_MODEL_API_KEY="b2cbf2e6e78c46b2a6e13b44a8cd9887.1tbiu9JwkNp9rpX7"
$env:MIDSCENE_MODEL_NAME="glm-4.6v"
$env:MIDSCENE_MODEL_FAMILY="glm-v"
npx tsx xx路径/demo.ts
```

20260316 14：12 成功跑通上述桥接模式

# 使用yaml模式

https://midscenejs.com/zh/yaml-script-runner.html

```powershell
npm install -g @midscene/cli
$env:MIDSCENE_MODEL_BASE_URL="https://api.z.ai/api/paas/v4"
$env:MIDSCENE_MODEL_API_KEY="b2cbf2e6e78c46b2a6e13b44a8cd9887.1tbiu9JwkNp9rpX7"
$env:MIDSCENE_MODEL_NAME="glm-4.6v"
$env:MIDSCENE_MODEL_FAMILY="glm-v"
midscene task.yaml --headed
```

注意：如果使用 yaml 模式，则在12306的出发地输入文本（aiInput）时无法触发下拉列表。但是 aiKeyboardPress（只能输入一个字符）可以触发下拉列表https://midscenejs.com/zh/api.html#agentaikeyboardpress。——但是我现在需要纠结这个问题吗？这个情况太极端了，不需要吧。