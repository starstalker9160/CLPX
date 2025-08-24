import asyncio
import websockets
import pyperclip

async def listen(ws):
    async for message in ws:
        print(f"Received from server: {message}")
        pyperclip.copy(message)

async def send_input(ws):
    loop = asyncio.get_running_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "Enter message: ")
        message = str(user_input).strip()
        await ws.send(message)
        print(f"Sent to server: {message}")

async def main():
    uri = "ws://localhost:6262/ws"
    async with websockets.connect(uri) as ws:
        await asyncio.gather(
            listen(ws),
            send_input(ws)
        )

if __name__ == '__main__':
    asyncio.run(main())
