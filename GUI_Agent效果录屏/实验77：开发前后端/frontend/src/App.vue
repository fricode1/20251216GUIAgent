<template>
  <div id="app">
    <div class="header">
      <h1>行人交通违法查询平台</h1>
    </div>

    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.type]"
        >
          <div class="message-content">
            <template v-if="msg.type === 'user'">
              <p>{{ msg.text }}</p>
            </template>
            <template v-else>
              <p>{{ msg.text }}</p>
              <div v-if="msg.images && msg.images.length > 0" class="images-grid">
                <div v-for="(img, imgIndex) in msg.images" :key="imgIndex" class="image-card">
                  <img :src="getImageUrl(img.minio_path)" alt="违法记录" @error="handleImageError" />
                  <div class="image-info">
                    <p><strong>时间:</strong> {{ img.time }}</p>
                    <p><strong>地点:</strong> {{ img.location }}</p>
                    <p><strong>姓名:</strong> {{ img.name }}</p>
                    <p><strong>身份证号:</strong> {{ img.id_number }}</p>
                  </div>
                </div>
              </div>
              <div v-if="msg.loading" class="loading">正在查询中...</div>
            </template>
          </div>
        </div>
      </div>

      <div class="input-area">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="输入问题，例如：查询新华路昨天的行人违章"
          :disabled="isLoading"
        />
        <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
          {{ isLoading ? '查询中...' : '发送' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const userInput = ref('')
const messages = ref([])
const messagesContainer = ref(null)
const isLoading = ref(false)

// Scroll to bottom of messages
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Get image URL from MinIO path
const getImageUrl = (minioPath) => {
  // Assuming MinIO serves files via HTTP
  // Format: bucket/object_name
  return `http://localhost:9000/${minioPath}`
}

// Handle image load error
const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/300x200?text=Image+Not+Available'
}

// Send message to backend
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const question = userInput.value.trim()

  // Add user message
  messages.value.push({
    type: 'user',
    text: question
  })

  userInput.value = ''
  isLoading.value = true
  await scrollToBottom()

  // Add bot message with loading state
  const botMessageIndex = messages.value.length
  messages.value.push({
    type: 'bot',
    text: `正在查询"${question}"的违章记录...`,
    images: [],
    loading: true
  })
  await scrollToBottom()

  try {
    // Make SSE request to backend
    await axios({
      method: 'post',
      url: `${API_BASE_URL}/api/query`,
      data: { question },
      responseType: 'stream',
      headers: {
        'Content-Type': 'application/json',
      },
      onDownloadProgress: (progressEvent) => {
        const xhr = progressEvent.event.target
        const { responseText } = xhr
        const lines = responseText.split('\n')

        lines.forEach(line => {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))

              if (data.status === 'success') {
                // Update bot message with new image
                messages.value[botMessageIndex].images.push(data)
                messages.value[botMessageIndex].loading = false
                scrollToBottom()
              } else if (data.status === 'error') {
                console.error('Error:', data.message)
              }
            } catch (e) {
              console.error('Parse error:', e)
            }
          }
        })
      }
    })

    messages.value[botMessageIndex].loading = false
    messages.value[botMessageIndex].text = `查询完成！找到 ${messages.value[botMessageIndex].images.length} 条违章记录：`

  } catch (error) {
    console.error('Query error:', error)
    messages.value[botMessageIndex].loading = false
    messages.value[botMessageIndex].text = `查询失败: ${error.message}`
  }

  isLoading.value = false
  await scrollToBottom()
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header h1 {
  margin: 0;
  font-size: 28px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  word-wrap: break-word;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message.bot .message-content {
  background: #f1f1f1;
  color: #333;
}

.message-content p {
  margin: 0 0 10px 0;
  line-height: 1.5;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 10px;
}

.image-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.image-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.image-info {
  padding: 10px;
  font-size: 12px;
}

.image-info p {
  margin: 4px 0;
  color: #666;
}

.loading {
  color: #999;
  font-style: italic;
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading::after {
  content: '';
  width: 12px;
  height: 12px;
  border: 2px solid #999;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.input-area {
  display: flex;
  padding: 20px;
  gap: 10px;
  border-top: 1px solid #eee;
  background: white;
}

.input-area input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.input-area input:focus {
  border-color: #667eea;
}

.input-area input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.input-area button {
  padding: 12px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.input-area button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.input-area button:active:not(:disabled) {
  transform: translateY(0);
}

.input-area button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
