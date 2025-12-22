import asyncio
from cdp_use.client import CDPClient

async def main():
    # 1. 连接到浏览器
    # 注意：这里的 URL 建议换成不带具体 ID 的，或者确保 ID 是正确的
    # 通常可以用 ws://127.0.0.1:9222/devtools/browser/xxx
    uri = "ws://[::1]:9222/devtools/browser/7119b24e-4638-4d1f-89ec-06fae1f66be5"
    
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
        # flatten=True 允许我们在同一个连接里通过 session_id 发送指令
        attachment = await cdp.send.Target.attachToTarget({
            "targetId": target_id,
            "flatten": True
        })

                
        sid = attachment['sessionId']

        # 4. 启用必要的域
        await cdp.send.DOM.enable({}, session_id=sid)

        # 5. 获取页面文档根节点
        doc = await cdp.send.DOM.getDocument({"depth": 0}, session_id=sid)
        root_node_id = doc['root']['nodeId']

        # 6. 使用选择器找到你要点击的元素
        # 示例：点击知乎页面上的“发现”链接，或者简单地找第一个 <a> 标签
        selector = "a" # 你可以修改为具体的 CSS 选择器，如 ".AppHeader-navItem"
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
        box = await cdp.send.DOM.getBoxModel({"nodeId": node_id}, session_id=sid)
        # quad 包含 8 个值，代表 4 个点的 [x, y] 坐标
        # content 是元素的实际内容区域
        quad = box['model']['content']
        # 计算中心点坐标
        center_x = (quad[0] + quad[2] + quad[4] + quad[6]) / 4
        center_y = (quad[1] + quad[3] + quad[5] + quad[7]) / 4

        print(f"找到元素，坐标中心点: ({center_x}, {center_y})，准备模拟点击...")

        # 8. 模拟鼠标移动到位置
        await cdp.send.Input.dispatchMouseEvent({
            "type": "mouseMoved",
            "x": center_x,
            "y": center_y,
            "session_id": sid # 注意：有些封装库需要把 session_id 放在 params 里或作为方法参数
        }, session_id=sid)

        # 9. 模拟鼠标按下 (mousePressed)
        await cdp.send.Input.dispatchMouseEvent({
            "type": "mousePressed",
            "x": center_x,
            "y": center_y,
            "button": "left",
            "clickCount": 1
        }, session_id=sid)

        # 10. 模拟鼠标弹起 (mouseReleased)
        await cdp.send.Input.dispatchMouseEvent({
            "type": "mouseReleased",
            "x": center_x,
            "y": center_y,
            "button": "left",
            "clickCount": 1
        }, session_id=sid)

        print("点击指令已发送！")
        # 稍微等一下看看效果
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())