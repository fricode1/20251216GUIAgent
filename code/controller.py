import asyncio
from computer import Computer

async def main():
    computer = Computer(
        os_type="windows",
        use_host_computer_server=True
    )
    try:
        await computer.run()
        await computer.interface.press("win")
        await computer.interface.type_text("Hello!")
    finally:
        await computer.stop()

if __name__ == "__main__":
    asyncio.run(main())
