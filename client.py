import sys, subprocess, asyncio

try:
    import websockets
    import pyperclip
except ImportError as e:
    missing = e.name
    pkg = {"websockets": "websockets", "pyperclip": "pyperclip"}.get(missing, missing)
    print(f"Missing module: {missing} (pip package: {pkg})")
    o = input(f"Install {pkg}? (y/n): ").strip().lower()
    if o == "y":
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print(f"{pkg} installed. Please rerun the script.")
    else:
        sys.exit(1)


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

async def main(uri: str):
    async with websockets.connect(uri) as ws:
        await asyncio.gather(
            listen(ws),
            send_input(ws)
        )

if __name__ == '__main__':
    try:
        asyncio.run(main(f"ws://{input("ip: ")}:{input("port: ")}/ws"))
    except KeyboardInterrupt:
        print("")
