import asyncio
from cdp_use.client import CDPClient

async def main():
    # 1. 连接到浏览器
    uri = "ws://127.0.0.1:9222/devtools/browser/4ca7aed5-583e-47fa-9d3e-99cffac381a5"
    
    async with CDPClient(uri) as cdp:
        # 2. 获取所有目标并找到“页面”类型的目标
        targets = await cdp.send.Target.getTargets()
        page_target = None
        for target in targets["targetInfos"]:
            if target['type'] == 'page':
                page_target = target
                break
        
        if not page_target:
            print("未找到可操作的页面标签页")
            return

        target_id = page_target['targetId']
        print(f"正在操作目标: {page_target['title']} (ID: {target_id})")

        # 3. 附着到目标获取 session_id
        attachment = await cdp.send.Target.attachToTarget({
            "targetId": target_id,
            "flatten": True
        })
        sid = attachment['sessionId']

        # 4. 启用必要的域
        await cdp.send.DOM.enable({}, session_id=sid)

        # 5. 获取根节点并找到目标元素
        doc = await cdp.send.DOM.getDocument({"depth": 0}, session_id=sid)
        root_node_id = doc['root']['nodeId']
        selector = '#train_date'

        try:
            target_node = await cdp.send.DOM.querySelector({
                "nodeId": root_node_id,
                "selector": selector
            }, session_id=sid)
            node_id = target_node['nodeId']
        except Exception as e:
            print(f"未找到选择器为 '{selector}' 的元素: {e}")
            return

        result = await cdp.send.Runtime.evaluate({
            "expression": """
                (function() {
                    const focused = document.activeElement;
                    if (!focused) return null;
                    // 返回焦点元素的标签名、ID 和类名
                    return {
                        tagName: focused.tagName,
                        id: focused.id,
                        className: focused.className,
                        outerHTML: focused.outerHTML.substring(0, 100)  // 截取部分 HTML
                    };
                })()
            """,
            "returnByValue": True
        }, session_id=sid)

        if result["result"]["value"]:
            focused_info = result["result"]["value"]
            print("当前焦点元素信息：")
            print(f"标签名: {focused_info['tagName']}")
            print(f"ID: {focused_info['id']}")
            print(f"类名: {focused_info['className']}")
            print(f"HTML 片段: {focused_info['outerHTML']}")
        else:
            print("当前无焦点元素")

        # 6. 首先聚焦到该元素（确保键盘输入能送达目标）
        # await cdp.send.DOM.focus({"nodeId": node_id}, session_id=sid)
        # print(f"已聚焦到元素: {selector}")

        # 7. 模拟键盘按下 '2' (keyDown)
        await cdp.send.Input.dispatchKeyEvent({
            'type': 'keyDown',
            'key': '2',
            'code': 'Digit2',
            'modifiers': 0,
            'windowsVirtualKeyCode': 50,
            'nativeVirtualKeyCode': 50,
            'text': '2' # 某些情况下需要 text 字段
        }, session_id=sid)

        # 8. 模拟键盘弹起 '2' (keyUp) - 完整的按键动作通常需要这一步
        await cdp.send.Input.dispatchKeyEvent({
            'type': 'keyUp',
            'key': '2',
            'code': 'Digit2',
            'modifiers': 0,
            'windowsVirtualKeyCode': 50,
            'nativeVirtualKeyCode': 50,
        }, session_id=sid)

        print("按键 '2' 已发送！")
        
        # 稍微等一下看看效果
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())