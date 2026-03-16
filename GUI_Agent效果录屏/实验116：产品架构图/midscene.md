# 桥接模式

```powershell
$env:MIDSCENE_MODEL_BASE_URL="https://api.z.ai/api/paas/v4"
$env:OPENAI_API_KEY="b2cbf2e6e78c46b2a6e13b44a8cd9887.1tbiu9JwkNp9rpX7"
$env:MIDSCENE_MODEL_NAME="openai:glm-4.6v"
$env:MIDSCENE_MODEL_FAMILY="openai:glm-v"
npx tsx xx路径/demo.ts
```

# 使用yaml模式

```powershell
npm install -D @midscene/cli
$env:MIDSCENE_MODEL_BASE_URL="https://api.z.ai/api/paas/v4"
$env:OPENAI_API_KEY="b2cbf2e6e78c46b2a6e13b44a8cd9887.1tbiu9JwkNp9rpX7"
$env:MIDSCENE_MODEL_NAME="openai:glm-4.6v"
npx midscene xx目录 task.yaml
```