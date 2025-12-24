import asyncio
from cdp_use.client import CDPClient

async def check_focus(cdp, sid, step_name):
    """查看并打印当前焦点情况"""
    result = await cdp.send.Runtime.evaluate({
        "expression": """
            (function() {
                const focused = document.activeElement;
                if (!focused || focused === document.body) return "无焦点 (或在 body)";
                return {
                    tagName: focused.tagName,
                    id: focused.id,
                    className: focused.className,
                    outerHTML: focused.outerHTML.substring(0, 100)
                };
            })()
        """,
        "returnByValue": True
    }, session_id=sid)

    print(f"\n[状态检查] {step_name}")
    val = result["result"].get("value")
    if isinstance(val, dict):
        print(f"  - 焦点位置: <{val['tagName']}> ID: '{val['id']}'")
    else:
        print(f"  - {val}")
    print("-" * 40)

async def main():
    # 注意：请确保 Chrome 端口和 ID 正确
    uri = "ws://127.0.0.1:9222/devtools/browser/6c0da9d6-2aaa-4dee-84c2-86a221960ffc"
    
    async with CDPClient(uri) as cdp:
        # 1. 初始化连接
        targets = await cdp.send.Target.getTargets()
        page_target = next(t for t in targets["targetInfos"] if t['type'] == 'page')
        attachment = await cdp.send.Target.attachToTarget({"targetId": page_target['targetId'], "flatten": True})
        sid = attachment['sessionId']

        await cdp.send.Runtime.enable({}, session_id=sid)
        # DOM 域在获取 objectId 时其实不是必须的，但建议开启
        await cdp.send.DOM.enable({}, session_id=sid)

        # ---------------------------------------------------------
        # 步骤 1: 直接获取元素的 objectId 并聚焦
        # ---------------------------------------------------------
        selector = "#train_date"
        print(f"查找元素: {selector}...")
        
        # 使用 Runtime.evaluate 直接获取元素的 RemoteObject (包含 objectId)
        # 这种方式比 DOM.querySelector 更稳定
        find_res = await cdp.send.Runtime.evaluate({
            "expression": f"document.querySelector('{selector}')",
            "includeCommandLineAPI": True
        }, session_id=sid)

        remote_obj = find_res.get('result', {})
        if remote_obj.get('subtype') == 'null' or 'objectId' not in remote_obj:
            print(f"错误: 页面上未找到 {selector}")
            return

        object_id = remote_obj['objectId']

        # 聚焦元素 (通过 JS 确保成功)
        await cdp.send.Runtime.callFunctionOn({
            "functionDeclaration": "function() { this.focus(); }",
            "objectId": object_id
        }, session_id=sid)
        print("已尝试执行 focus()")

        # ---------------------------------------------------------
        # 步骤 2: 查看焦点 (确认清除前状态)
        # ---------------------------------------------------------
        await check_focus(cdp, sid, "执行清除前")

        # ---------------------------------------------------------
        # 步骤 3: 执行清除文本的代码
        # ---------------------------------------------------------
        print("正在执行清除文本的 JS 代码...")
        clear_js = """
            function() {
                const hasContentEditable = this.getAttribute('contenteditable') === 'true' ||
                                        this.getAttribute('contenteditable') === '' ||
                                        this.isContentEditable === true;

                if (hasContentEditable) {
                    while (this.firstChild) {
                        this.removeChild(this.firstChild);
                    }
                    this.textContent = "";
                    this.innerHTML = "";

                    this.focus();
                    const selection = window.getSelection();
                    const range = document.createRange();
                    range.setStart(this, 0);
                    range.setEnd(this, 0);
                    selection.removeAllRanges();
                    selection.addRange(range);

                    this.dispatchEvent(new Event("input", { bubbles: true }));
                    this.dispatchEvent(new Event("change", { bubbles: true }));
                    return "cleared contenteditable";
                } else if (this.value !== undefined) {
                    try {
                        this.select(); // 可能是这行或后续赋值导致焦点丢失
                    } catch (e) {}
                    this.value = "";
                    this.dispatchEvent(new Event("input", { bubbles: true }));
                    this.dispatchEvent(new Event("change", { bubbles: true }));
                    return "cleared input value";
                }
                return "not supported type";
            }
        """

        await cdp.send.Runtime.callFunctionOn({
            "functionDeclaration": clear_js,
            "objectId": object_id,
            "returnByValue": True,
        }, session_id=sid)

        # ---------------------------------------------------------
        # 步骤 4: 再次查看焦点 (观察复现结果)
        # ---------------------------------------------------------
        await asyncio.sleep(0.5) 
        await check_focus(cdp, sid, "执行清除后")

if __name__ == "__main__":
    asyncio.run(main())