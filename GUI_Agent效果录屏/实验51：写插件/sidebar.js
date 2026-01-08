// 获取DOM元素
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// DeepSeek API 配置
const API_CONFIG = {
  baseURL: 'https://api.deepseek.com',
  apiKey: 'sk-6fda4f18a54140c6ae408fdd13cfe97d',
  model: 'deepseek-chat'
};

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

// 调用 DeepSeek API
async function callDeepSeekAPI(messages) {
  try {
    const response = await fetch(`${API_CONFIG.baseURL}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_CONFIG.apiKey}`
      },
      body: JSON.stringify({
        model: API_CONFIG.model,
        messages: messages,
        temperature: 0.7,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// 获取当前标签页的 DOM 内容
async function getCurrentTabDOM() {
  try {
    // 获取当前活动标签页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab || !tab.id) {
      throw new Error('无法获取当前标签页');
    }

    // 在标签页中执行脚本来获取 DOM
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        return document.documentElement.outerHTML;
      }
    });

    return results[0].result;
  } catch (error) {
    console.error('获取 DOM 失败:', error);
    throw error;
  }
}

// 发送消息
async function sendMessage() {
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

  // 检查是否输入了 "DOM"
  if (message.toUpperCase() === 'DOM') {
    // 显示"正在获取..."提示
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message bot';
    thinkingDiv.innerHTML = `
      <div class="sender">Bot</div>
      <div class="content">📄 正在获取 DOM 内容...</div>
    `;
    chatContainer.appendChild(thinkingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
      // 获取当前标签页的 DOM 内容
      const domContent = await getCurrentTabDOM();

      // 移除"正在获取..."提示
      thinkingDiv.remove();

      // 添加 DOM 内容（截取前5000个字符以避免消息过长）
      const truncatedDOM = domContent.length > 5000
        ? domContent.substring(0, 5000) + '\n\n... (内容过长，已截断)'
        : domContent;

      addMessage(`📄 **当前标签页 DOM 内容：**\n\n\`\`\`html\n${truncatedDOM}\n\`\`\``, false);
    } catch (error) {
      // 移除"正在获取..."提示
      thinkingDiv.remove();

      // 显示错误消息
      addMessage(`❌ 获取 DOM 失败: ${error.message}`, false);
    } finally {
      // 重新启用发送按钮
      sendButton.disabled = false;
      messageInput.focus();
    }
    return;
  }

  // 显示"正在思考..."提示
  const thinkingDiv = document.createElement('div');
  thinkingDiv.className = 'message bot';
  thinkingDiv.innerHTML = `
    <div class="sender">Bot</div>
    <div class="content">🤔 正在思考...</div>
  `;
  chatContainer.appendChild(thinkingDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    // 调用 API
    const response = await callDeepSeekAPI(chatHistory);

    // 移除"正在思考..."提示
    thinkingDiv.remove();

    // 添加 Bot 回复
    addMessage(response, false);
  } catch (error) {
    // 移除"正在思考..."提示
    thinkingDiv.remove();

    // 显示错误消息
    addMessage(`❌ 请求失败: ${error.message}`, false);
  } finally {
    // 重新启用发送按钮
    sendButton.disabled = false;
    messageInput.focus();
  }
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
