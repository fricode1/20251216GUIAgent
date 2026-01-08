// 当扩展安装时，打开侧边栏
chrome.runtime.onInstalled.addListener(() => {
  console.log('HelloWorld Sidebar extension installed');
});

// 当用户点击扩展图标时，打开侧边栏
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId });
});
