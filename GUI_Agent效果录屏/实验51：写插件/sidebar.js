// 获取DOM元素
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// 存储对话历史
let chatHistory = [];
let isFirstMessage = true;

// 添加消息到聊天界面
function addMessage(content, isUser) {
  // 移除空状态提示
  if (isFirstMessage) {
    const emptyState = chatContainer.querySelector('.empty-state');
    if (emptyState) {
      emptyState.remove();
    }
    isFirstMessage = false;
  }

  // 创建消息元素
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

  const senderDiv = document.createElement('div');
  senderDiv.className = 'sender';
  senderDiv.textContent = isUser ? '你' : 'Bot';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  contentDiv.textContent = content;

  messageDiv.appendChild(senderDiv);
  messageDiv.appendChild(contentDiv);
  chatContainer.appendChild(messageDiv);

  // 滚动到底部
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // 保存到历史
  chatHistory.push({
    role: isUser ? 'user' : 'assistant',
    content: content
  });
}

// 发送消息
function sendMessage() {
  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  // 添加用户消息
  addMessage(message, true);

  // 清空输入框
  messageInput.value = '';

  // 禁用发送按钮
  sendButton.disabled = true;

  // 模拟回复（回显相同内容）
  setTimeout(() => {
    addMessage(message, false);
    sendButton.disabled = false;
    messageInput.focus();
  }, 500);
}

// 事件监听
sendButton.addEventListener('click', sendMessage);

// 回车发送消息
messageInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// 输入时启用/禁用发送按钮
messageInput.addEventListener('input', () => {
  sendButton.disabled = !messageInput.value.trim();
});

// 初始化时禁用发送按钮
sendButton.disabled = true;

// 页面加载完成后聚焦输入框
window.addEventListener('load', () => {
  messageInput.focus();
});
