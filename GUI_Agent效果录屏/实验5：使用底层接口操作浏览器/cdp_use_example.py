
import asyncio
from cdp_use.client import CDPClient

async def main():
    # Connect to Chrome DevTools
    async with CDPClient("ws://[::1]:9222/devtools/browser/7119b24e-4638-4d1f-89ec-06fae1f66be5") as cdp:
        # Get all browser targets with full type safety
        targets = await cdp.send.Target.getTargets()
        print(f"Found {len(targets['targetInfos'])} targets")
        for target in targets["targetInfos"]:
            print(f"目标ID: {target['targetId']}, 标题: {target['title']}, URL: {target['url']}")

asyncio.run(main())
