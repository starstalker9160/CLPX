import sys, subprocess, asyncio, socket

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

IP, PORT = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(5)

print("Locating CLPX server")
for i in range(3):
    print(f"Attempt ({i + 1}/3)...")
    try:
        sock.sendto("DISCOVER_clpx.services.homelab.ree".encode("utf-8"), ('255.255.255.255', 6969))
        data, addr = sock.recvfrom(1024)
        print(f"Found server at {data.decode("utf-8")}")
        IP, PORT = data.decode("utf-8").rstrip("/").split(":")
        PORT = int(PORT)
        break
    except socket.timeout:
        print("No response, retrying...")


async def listen(ws):
    async for message in ws:
        print(f"\nReceived from server: {message}")
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
        if not IP or not PORT:
            print("Did not find a CLPX server.")
            sys.exit(1)
        asyncio.run(main(f"ws://{IP}:{PORT}/ws"))
    except KeyboardInterrupt:
        print("Program interrupted by user")
