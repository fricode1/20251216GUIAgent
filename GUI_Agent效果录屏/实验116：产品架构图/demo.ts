import { configure, AgentOverChromeBridge } from "@midscene/web/bridge-mode";

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