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

// 系统提示词
const SYSTEM_PROMPT = `你是一个智能网页助手，可以帮助用户与当前浏览器标签页进行交互。

你拥有以下能力：
1. 查看当前网页的所有可交互元素（按钮、链接、输入框等）
2. 点击网页上的任何可交互元素
3. 导航到指定的网址

使用规则：
- 当用户询问关于网页元素、想要点击按钮、提交表单、导航链接等操作时，先调用 get_interactive_elements 工具查看可用的元素
- 获取元素列表后，根据用户的请求选择合适的元素 ID
- 使用 click_element 工具点击目标元素
- 当用户想要访问某个网站时，使用 navigate_to_url 工具导航到指定网址
- 完成操作后，向用户说明执行了什么操作以及结果

示例对话：
用户：帮我点击登录按钮
你：[调用 get_interactive_elements] → [看到登录按钮 ID 是 5] → [调用 click_element(5)] → [回复用户：已成功点击登录按钮]

用户：打开百度
你：[调用 navigate_to_url("https://www.baidu.com")] → [回复用户：已导航到百度]

用户：页面上有什么可以点击的？
你：[调用 get_interactive_elements] → [回复用户：页面上有以下可交互元素...]

请自然、友好地与用户交流。主动使用工具来完成用户的需求。`;

let isFirstMessage = true;

// 定义可用的工具
const TOOLS = [
  {
    type: 'function',
    function: {
      name: 'get_interactive_elements',
      description: '获取当前网页标签页中的所有可交互元素（按钮、链接、输入框等）及其ID。当用户想了解页面内容或需要点击某个元素时调用此工具。',
      parameters: {
        type: 'object',
        properties: {},
        required: []
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'click_element',
      description: '点击当前网页中指定ID的可交互元素。在调用此工具前，应该先调用 get_interactive_elements 获取元素列表。',
      parameters: {
        type: 'object',
        properties: {
          element_id: {
            type: 'integer',
            description: '要点击的元素ID（通过get_interactive_elements获取）'
          }
        },
        required: ['element_id']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'navigate_to_url',
      description: '在当前浏览器标签页中导航到指定的网址。当用户想要访问某个网站时调用此工具。',
      parameters: {
        type: 'object',
        properties: {
          url: {
            type: 'string',
            description: '要导航到的网址（需要包含协议，如 https://www.baidu.com）'
          }
        },
        required: ['url']
      }
    }
  }
];

// 添加消息到聊天界面
// addToHistory 参数：是否将消息添加到对话历史（默认 true）
function addMessage(content, isUser, addToHistory = true) {
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
  // 如果是用户消息或者是工具调用结果，使用纯文本
  // 如果是 Bot 的普通回复，使用 Markdown 渲染
  const isToolOutput = content.startsWith('📄') || content.startsWith('✅') || content.startsWith('❌') || content.startsWith('🖱️') || content.startsWith('🔧');

  if (!isUser && !isToolOutput) {
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

  // 保存到历史（如果需要）
  if (addToHistory) {
    chatHistory.push({
      role: isUser ? 'user' : 'assistant',
      content: content
    });
  }
}

// 执行工具调用
async function executeToolCall(toolName, toolArgs) {
  console.log('执行工具调用:', toolName, toolArgs);

  if (toolName === 'get_interactive_elements') {
    const elements = await getCurrentTabDOM();

    let output = `🔧 **工具调用结果 - get_interactive_elements**\n\n`;
    output += `📄 当前标签页的可交互元素（共 ${elements.length} 个）：\n\n`;

    elements.forEach(el => {
      let desc = `[${el.id}] ${el.tag}`;
      if (el.type) desc += `[type="${el.type}"]`;
      if (el.role) desc += `[role="${el.role}"]`;
      if (el.text) {
        desc += ` - "${el.text}${el.text.length >= 50 ? '...' : ''}"`;
      }
      if (el.placeholder) {
        desc += ` [placeholder: "${el.placeholder}"]`;
      }
      if (el.href) {
        desc += ` → ${el.href}`;
      }
      if (el.idAttr) desc += ` #${el.idAttr}`;
      if (el.className) desc += ` .${el.className.split(' ').join('.')}`;

      output += desc + '\n';
    });

    output += `\n💡 提示：你可以使用这些元素 ID 来引用特定元素`;

    return { success: true, result: output, elements: elements };
  }
  else if (toolName === 'click_element') {
    const elementId = toolArgs.element_id;
    const clickResult = await clickElement(elementId);

    if (clickResult.success) {
      const output = `🔧 **工具调用结果 - click_element**\n\n✅ ${clickResult.message}`;
      return { success: true, result: output };
    } else {
      const output = `🔧 **工具调用结果 - click_element**\n\n❌ 点击失败: ${clickResult.error}`;
      return { success: false, result: output, error: clickResult.error };
    }
  }
  else if (toolName === 'navigate_to_url') {
    const url = toolArgs.url;
    const navResult = await navigateToUrl(url);

    if (navResult.success) {
      const output = `🔧 **工具调用结果 - navigate_to_url**\n\n✅ ${navResult.message}`;
      return { success: true, result: output };
    } else {
      const output = `🔧 **工具调用结果 - navigate_to_url**\n\n❌ 导航失败: ${navResult.error}`;
      return { success: false, result: output, error: navResult.error };
    }
  }

  return { success: false, result: `❌ 未知的工具: ${toolName}` };
}

// 调用 DeepSeek API（支持工具调用）
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
        tools: TOOLS,
        temperature: 0.7,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].message;
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

// 导航到指定网址
async function navigateToUrl(url) {
  try {
    // 获取当前活动标签页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab || !tab.id) {
      throw new Error('无法获取当前标签页');
    }

    // 验证并格式化 URL
    let formattedUrl = url.trim();
    if (!formattedUrl.startsWith('http://') && !formattedUrl.startsWith('https://')) {
      formattedUrl = 'https://' + formattedUrl;
    }

    // 更新标签页的 URL
    await chrome.tabs.update(tab.id, { url: formattedUrl });

    return {
      success: true,
      url: formattedUrl,
      message: `已导航到: ${formattedUrl}`
    };
  } catch (error) {
    console.error('导航失败:', error);
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
    let maxIterations = 10; // 防止无限循环
    let currentMessage = message;

    while (maxIterations-- > 0) {
      // 构建完整的消息历史（包含系统提示词）
      const messagesWithSystem = [
        { role: 'system', content: SYSTEM_PROMPT },
        ...chatHistory
      ];

      // 调用 API
      const response = await callDeepSeekAPI(messagesWithSystem);

      // 检查是否需要调用工具
      if (response.tool_calls && response.tool_calls.length > 0) {
        // AI 请求调用工具
        const toolCall = response.tool_calls[0];
        const toolName = toolCall.function.name;
        const toolArgs = JSON.parse(toolCall.function.arguments);

        console.log('AI 请求调用工具:', toolName, toolArgs);

        // 将 assistant 的 tool_calls 消息添加到历史
        chatHistory.push({
          role: 'assistant',
          content: response.content || null,
          tool_calls: response.tool_calls
        });

        // 执行工具调用
        const toolResult = await executeToolCall(toolName, toolArgs);

        // 显示工具调用结果（不添加到历史，因为我们会以特定格式添加）
        addMessage(toolResult.result, false, false);

        // 将工具结果添加到历史
        chatHistory.push({
          role: 'tool',
          tool_call_id: toolCall.id,
          content: JSON.stringify(toolResult)
        });

        // 继续循环，让 AI 根据工具结果决定下一步
        continue;
      } else {
        // AI 返回了普通文本回复
        // 移除"正在思考..."提示
        thinkingDiv.remove();

        // 添加 Bot 回复到聊天界面和历史
        if (response.content) {
          addMessage(response.content, false, true);
        } else {
          // 如果没有内容，也要添加一个空的 assistant 消息
          chatHistory.push({
            role: 'assistant',
            content: ''
          });
        }

        // 结束循环
        break;
      }
    }

    if (maxIterations <= 0) {
      addMessage('⚠️ 达到最大迭代次数，任务可能未完成', false);
    }
  } catch (error) {
    // 移除"正在思考..."提示
    if (thinkingDiv.parentNode) {
      thinkingDiv.remove();
    }

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
