import { AgentOverChromeBridge } from "@midscene/web/bridge-mode";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

Promise.resolve(
  (async () => {
    const agent = new AgentOverChromeBridge();
    await agent.connectNewTabWithUrl("https://www.12306.cn/index/ ");
    await sleep(3000);

    // ========== 设置出发地：北京北 ==========
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
        fromInput.dispatchEvent(new Event('change', { bubbles: true }));
        
        // 输入"北京北" - 逐字输入以触发 keyup 事件
        const text = '北京北';
        
        // 方法1: 使用 KeyboardEvent 模拟真实输入（推荐）
        for (let i = 0; i < text.length; i++) {
          const char = text[i];
          
          // 创建 keydown 事件
          const keydownEvent = new KeyboardEvent('keydown', {
            key: char,
            code: 'Key' + char.toUpperCase(),
            keyCode: char.charCodeAt(0),
            bubbles: true,
            cancelable: true
          });
          fromInput.dispatchEvent(keydownEvent);
          
          // 设置值
          const currentValue = fromInput.value + char;
          const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 
            'value'
          ).set;
          setter.call(fromInput, currentValue);
          
          // 创建 input 事件
          fromInput.dispatchEvent(new Event('input', { bubbles: true }));
          
          // 创建 keyup 事件（关键！触发下拉框）
          const keyupEvent = new KeyboardEvent('keyup', {
            key: char,
            code: 'Key' + char.toUpperCase(),
            keyCode: char.charCodeAt(0),
            bubbles: true,
            cancelable: true
          });
          fromInput.dispatchEvent(keyupEvent);
          
          // 短暂延迟，模拟真实打字间隔
          const delay = 50 + Math.random() * 50;
          const start = Date.now();
          while (Date.now() - start < delay) {}
        }
        
        // 额外触发 composition 事件（某些框架需要）
        fromInput.dispatchEvent(new Event('compositionend', { bubbles: true }));
        
        // 最终触发 change 和 blur
        fromInput.dispatchEvent(new Event('change', { bubbles: true }));
        
        // 保持聚焦
        fromInput.focus();
    
        return { 
          success: true, 
          type: 'from',
          value: fromInput.value,
          element: fromInput.id || fromInput.className || fromInput.tagName
        };
      })()
    `);

    await sleep(800);
    
    // 如果下拉框出现，选择"北京北"
    await agent.ai('如果出现了城市下拉选项，点击"北京北"');
    
    await sleep(500);

    // ========== 设置到达地：深圳北 ==========
    await agent.evaluateJavaScript(`
      (function() {
        // 12306 到达地输入框选择器（可能需要根据实际页面调整）
        const toInput = document.querySelector('#toStationText') || 
                       document.querySelector('.input-in[tostation]') ||
                       document.querySelector('input[placeholder*="到达"]') ||
                       document.querySelector('#toStation') ||
                       document.querySelector('input[name="toStation"]');
        
        if (!toInput) {
          return { success: false, error: '未找到到达地输入框' };
        }
        
        // 聚焦并点击
        toInput.focus();
        toInput.click();
        
        // 清除原有内容
        toInput.value = '';
        toInput.dispatchEvent(new Event('input', { bubbles: true }));
        toInput.dispatchEvent(new Event('change', { bubbles: true }));
        
        // 输入"深圳北" - 逐字输入以触发 keyup 事件
        const text = '深圳北';
        
        // 使用 KeyboardEvent 模拟真实输入
        for (let i = 0; i < text.length; i++) {
          const char = text[i];
          
          // 创建 keydown 事件
          const keydownEvent = new KeyboardEvent('keydown', {
            key: char,
            code: 'Key' + char.toUpperCase(),
            keyCode: char.charCodeAt(0),
            bubbles: true,
            cancelable: true
          });
          toInput.dispatchEvent(keydownEvent);
          
          // 设置值
          const currentValue = toInput.value + char;
          const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 
            'value'
          ).set;
          setter.call(toInput, currentValue);
          
          // 创建 input 事件
          toInput.dispatchEvent(new Event('input', { bubbles: true }));
          
          // 创建 keyup 事件（关键！触发下拉框）
          const keyupEvent = new KeyboardEvent('keyup', {
            key: char,
            code: 'Key' + char.toUpperCase(),
            keyCode: char.charCodeAt(0),
            bubbles: true,
            cancelable: true
          });
          toInput.dispatchEvent(keyupEvent);
          
          // 短暂延迟，模拟真实打字间隔
          const delay = 50 + Math.random() * 50;
          const start = Date.now();
          while (Date.now() - start < delay) {}
        }
        
        // 额外触发 composition 事件
        toInput.dispatchEvent(new Event('compositionend', { bubbles: true }));
        
        // 最终触发 change 和 blur
        toInput.dispatchEvent(new Event('change', { bubbles: true }));
        
        // 保持聚焦
        toInput.focus();
    
        return { 
          success: true, 
          type: 'to',
          value: toInput.value,
          element: toInput.id || toInput.className || toInput.tagName
        };
      })()
    `);

    await sleep(800);
    
    // 如果下拉框出现，选择"深圳北"
    await agent.ai('如果出现了城市下拉选项，点击"深圳北"');
    
    await sleep(500);

    await agent.ai('将出发时间设置为 2026-03-20');

    await sleep(500);

    await agent.ai('点击查询按钮')

    await agent.ai('在弹出的查询结果中，为我购买一张车票。如需登录信息，选择扫码登录，过段时间便会登录成功。')

    await agent.destroy();
  })()
);