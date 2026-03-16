import { configure, AgentOverChromeBridge } from "@midscene/web/bridge-mode";

// --- 正确的配置方式 ---
configure({
  // 必须是 'openai', 'anthropic', 'google-vertex' 等其中之一
  modelFamily: 'openai', 
  
  // 如果你需要指定具体的模型名称（比如 glm-4.6v），请使用下面这个字段
  // 环境变量名通常是 MIDSCENE_MODEL_NAME
});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
Promise.resolve(
  (async () => {
    const agent = new AgentOverChromeBridge();

    // This will connect to a new tab on your desktop Chrome
    await agent.connectNewTabWithUrl("https://www.bing.com");

    // these are the same as normal Midscene agent
    await agent.ai('type "AI 101" and hit Enter');
    await sleep(3000);

    await agent.aiAssert("there are some search results");
    await agent.destroy();
  })()
);