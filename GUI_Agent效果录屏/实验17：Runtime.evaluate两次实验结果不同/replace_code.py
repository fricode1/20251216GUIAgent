import asyncio
from cdp_use.client import CDPClient

async def main():
    # 1. 连接到浏览器
    # 请确保 Chrome 已经以 --remote-debugging-port=9222 启动
    # 注意：这里的 ID 如果变化了，需要更新，或者使用 /json 接口动态获取
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

        # 3. 附着到该目标以获取 session_id
        attachment = await cdp.send.Target.attachToTarget({
            "targetId": target_id,
            "flatten": True
        })
        sid = attachment['sessionId']

        # 4. 启用必要的域
        await cdp.send.DOM.enable({}, session_id=sid)
        # 执行 JS 需要启用 Runtime 域
        await cdp.send.Runtime.enable({}, session_id=sid)

        # 5. 获取页面文档根节点
        doc = await cdp.send.DOM.getDocument({"depth": 0}, session_id=sid)
        root_node_id = doc['root']['nodeId']

        # 6. 使用选择器找到你要点击的元素
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

        # 7. 获取元素的坐标 (Box Model)
        try:
            box = await cdp.send.DOM.getBoxModel({"nodeId": node_id}, session_id=sid)
            quad = box['model']['content']
            center_x = (quad[0] + quad[2] + quad[4] + quad[6]) / 4
            center_y = (quad[1] + quad[3] + quad[5] + quad[7]) / 4
            print(f"找到元素，坐标中心点: ({center_x}, {center_y})")
        except Exception as e:
            print(f"无法获取元素坐标 (可能元素不可见): {e}")
            return

        # 8-10. 模拟点击
        # 移动
        await cdp.send.Input.dispatchMouseEvent({
            "type": "mouseMoved",
            "x": center_x,
            "y": center_y
        }, session_id=sid)

        # 按下
        await cdp.send.Input.dispatchMouseEvent({
            "type": "mousePressed",
            "x": center_x,
            "y": center_y,
            "button": "left",
            "clickCount": 1
        }, session_id=sid)

        # 弹起
        await cdp.send.Input.dispatchMouseEvent({
            "type": "mouseReleased",
            "x": center_x,
            "y": center_y,
            "button": "left",
            "clickCount": 1
        }, session_id=sid)

        print("点击指令已发送！")

        # 稍微等待点击后的反应
        await asyncio.sleep(1)

        # ---------------------------------------------------------
        # 11. 执行 JavaScript 代码
        # ---------------------------------------------------------
        print("准备执行 JS 代码...")
        
        # 这里定义你要执行的 JS 逻辑
        # 我们定义 el，并返回它的 id 以便在 Python 中确认
        js_code = """
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
        """

        eval_response = await cdp.send.Runtime.evaluate({
            "expression": js_code,
            "returnByValue": True  # 设为 True 才能直接拿到返回的字符串
        })

        # 解析返回结果
        if 'result' in eval_response:
            res_value = eval_response['result'].get('value')
            print(f"JS 执行结果: {res_value}")
        else:
            print("JS 执行出错:", eval_response)

        # 保持几秒查看效果
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())