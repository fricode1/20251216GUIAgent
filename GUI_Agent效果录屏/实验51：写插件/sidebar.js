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

  // 判断是否需要渲染 Markdown
  // 如果是用户消息或者是命令输出（DOM、click），使用纯文本
  // 如果是 Bot 的普通回复，使用 Markdown 渲染
  const isCommandOutput = content.startsWith('📄') || content.startsWith('✅') || content.startsWith('❌') || content.startsWith('🖱️');

  if (!isUser && !isCommandOutput) {
    // 使用 marked.js 渲染 Markdown
    contentDiv.className = 'content markdown-content';
    // 检查 marked 是否已加载
    if (typeof marked !== 'undefined') {
      contentDiv.innerHTML = marked.parse(content);
    } else {
      // 如果 marked 未加载，使用纯文本
      contentDiv.textContent = content;
    }
  } else {
    // 使用纯文本
    contentDiv.textContent = content;
  }

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

// 获取当前标签页的可交互元素
async function getCurrentTabDOM() {
  try {
    // 获取当前活动标签页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab || !tab.id) {
      throw new Error('无法获取当前标签页');
    }

    // 在标签页中执行脚本来获取可交互元素
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        // 定义可交互元素的选择器
        const interactiveSelectors = [
          'button',
          'a[href]',
          'input',
          'textarea',
          'select',
          '[contenteditable="true"]',
          '[role="button"]',
          '[role="link"]',
          '[role="textbox"]',
          '[onclick]',
          '[tabindex]:not([tabindex="-1"])'
        ];

        const elements = [];
        const seen = new Set();

        // 遍历所有选择器
        interactiveSelectors.forEach(selector => {
          const nodes = document.querySelectorAll(selector);
          nodes.forEach(element => {
            // 使用元素路径作为唯一标识
            const getPath = (el) => {
              if (el.id) {
                return `${el.tagName.toLowerCase()}#${el.id}`;
              }
              const path = [];
              let current = el;
              while (current && current !== document.body) {
                let selector = current.tagName.toLowerCase();
                if (current.id) {
                  selector += `#${current.id}`;
                  path.unshift(selector);
                  break;
                }
                if (current.className) {
                  const classes = current.className.split(' ').filter(c => c).join('.');
                  if (classes) {
                    selector += `.${classes}`;
                  }
                }
                path.unshift(selector);
                current = current.parentElement;
              }
              return path.join(' > ');
            };

            const path = getPath(element);

            // 避免重复
            if (seen.has(path)) return;
            seen.add(path);

            // 获取元素信息
            const info = {
              id: elements.length + 1,
              tag: element.tagName.toLowerCase(),
              type: element.getAttribute('type') || '',
              role: element.getAttribute('role') || '',
              text: element.textContent?.trim().substring(0, 50) || '',
              placeholder: element.getAttribute('placeholder') || '',
              href: element.getAttribute('href') || '',
              name: element.getAttribute('name') || '',
              idAttr: element.id || '',
              className: element.className || '',
              selector: path
            };

            elements.push(info);
          });
        });

        // 将元素列表存储在 window 对象中，供后续操作使用
        window.__interactiveElements = elements;

        return elements;
      }
    });

    return results[0].result;
  } catch (error) {
    console.error('获取 DOM 失败:', error);
    throw error;
  }
}

// 点击指定元素
async function clickElement(elementId) {
  try {
    // 获取当前活动标签页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab || !tab.id) {
      throw new Error('无法获取当前标签页');
    }

    // 在标签页中执行脚本来点击元素
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (id) => {
        // 从之前存储的元素列表中查找
        if (!window.__interactiveElements) {
          return { success: false, error: '未找到元素列表，请先执行 DOM 命令' };
        }

        const elementInfo = window.__interactiveElements.find(el => el.id === id);
        if (!elementInfo) {
          return { success: false, error: `未找到 ID 为 ${id} 的元素` };
        }

        // 使用选择器查找元素
        const element = document.querySelector(elementInfo.selector);
        if (!element) {
          return { success: false, error: `元素可能已从页面移除: ${elementInfo.selector}` };
        }

        // 滚动到元素可见
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // 高亮元素（临时添加边框）
        const originalStyle = element.style.cssText;
        element.style.cssText = 'border: 3px solid red !important; outline: 3px solid red !important;';

        // 延迟点击，让用户看到高亮
        setTimeout(() => {
          element.click();
          setTimeout(() => {
            element.style.cssText = originalStyle;
          }, 500);
        }, 300);

        return {
          success: true,
          element: elementInfo,
          message: `已点击元素 [${id}]: ${elementInfo.tag}`
        };
      },
      args: [elementId]
    });

    return results[0].result;
  } catch (error) {
    console.error('点击元素失败:', error);
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
      // 获取当前标签页的可交互元素
      const elements = await getCurrentTabDOM();

      // 移除"正在获取..."提示
      thinkingDiv.remove();

      // 格式化输出
      let output = `📄 **当前标签页的可交互元素（共 ${elements.length} 个）：**\n\n`;

      elements.forEach(el => {
        let desc = `[${el.id}] ${el.tag}`;

        // 添加类型或角色信息
        if (el.type) desc += `[type="${el.type}"]`;
        if (el.role) desc += `[role="${el.role}"]`;

        // 添加文本内容
        if (el.text) {
          desc += ` - "${el.text}${el.text.length >= 50 ? '...' : ''}"`;
        }

        // 添加 placeholder
        if (el.placeholder) {
          desc += ` [placeholder: "${el.placeholder}"]`;
        }

        // 添加 href（链接）
        if (el.href) {
          desc += ` → ${el.href}`;
        }

        // 添加 id/class 信息
        if (el.idAttr) desc += ` #${el.idAttr}`;
        if (el.className) desc += ` .${el.className.split(' ').join('.')}`;

        output += desc + '\n';
      });

      // 添加选择器说明
      output += `\n💡 提示：可以使用元素 ID 来引用特定元素`;

      addMessage(output, false);
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

  // 检查是否是 click 命令
  const clickMatch = message.match(/^click\((\d+)\)$/i);
  if (clickMatch) {
    const elementId = parseInt(clickMatch[1]);

    // 显示"正在点击..."提示
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message bot';
    thinkingDiv.innerHTML = `
      <div class="sender">Bot</div>
      <div class="content">🖱️ 正在点击元素 [${elementId}]...</div>
    `;
    chatContainer.appendChild(thinkingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
      // 点击元素
      const result = await clickElement(elementId);

      // 移除"正在点击..."提示
      thinkingDiv.remove();

      if (result.success) {
        addMessage(`✅ ${result.message}`, false);
      } else {
        addMessage(`❌ 点击失败: ${result.error}`, false);
      }
    } catch (error) {
      // 移除"正在点击..."提示
      thinkingDiv.remove();

      // 显示错误消息
      addMessage(`❌ 点击失败: ${error.message}`, false);
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
