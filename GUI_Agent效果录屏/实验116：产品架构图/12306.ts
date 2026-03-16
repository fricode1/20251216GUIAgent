import { AgentOverChromeBridge } from "@midscene/web/bridge-mode";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

Promise.resolve(
  (async () => {
    const agent = new AgentOverChromeBridge();
    await agent.connectNewTabWithUrl("https://www.12306.cn/index/");
    await sleep(3000);

    // 使用 evaluateJavaScript 精确操作 DOM
    await agent.evaluateJavaScript(`
      (function() {
        // 12306 出发地输入框选择器（可能需要根据实际页面调整）
        const fromInput = document.querySelector('#fromStationText') || 
                         document.querySelector('.input-in[fromstation]') ||
                         document.querySelector('input[placeholder*="出发"]') ||
                         document.querySelector('#fromStation');
        
        if (!fromInput) {
          return { success: false, error: '未找到出发地输入框' };
        }
        
        // 聚焦并点击
        fromInput.focus();
        fromInput.click();
        
        // 清除原有内容
        fromInput.value = '';
        fromInput.dispatchEvent(new Event('input', { bubbles: true }));
        
        // 输入"南京南"
        const text = '南京南';
        const setter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype, 
          'value'
        ).set;
        setter.call(fromInput, text);
    
        return { 
          success: true, 
          value: fromInput.value,
          element: fromInput.id || fromInput.className || fromInput.tagName
        };
      })()
    `);

    await sleep(1000);
    
    // 可能需要点击下拉选项
    await agent.ai('如果出现了下拉选项，点击"南京南"');
    
    await agent.destroy();
  })()
);