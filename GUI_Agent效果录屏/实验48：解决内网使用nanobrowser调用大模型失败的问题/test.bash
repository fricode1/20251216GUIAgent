# 1. 设定节点数量（修改这个数字来测试不同长度，比如 500, 1000, 3000, 5000）
COUNT=2000

# 2. 生成模拟 DOM 数据 (每个节点约 50 字节)
LONG_DOM=$(printf '{"role":"button","name":"test-node-%04d"},' $(seq 1 $COUNT))

# 3. 发送请求
curl -X POST "http://44.71.1.34:8088/lm/v2/chat/completions" \
  -H "Authorization: Bearer 172423d8-0ab8-4e60-659b-de3cda928f95" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"qwen3-235b-a22b\",
    \"messages\": [
      {
        \"role\": \"system\", 
        \"content\": \"You are a web navigator. Help me find the button.\"
      },
      {
        \"role\": \"user\", 
        \"content\": \"Current page tree: [$LONG_DOM]\"
      }
    ],
    \"temperature\": 0
  }" \
  -v