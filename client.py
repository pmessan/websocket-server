"""Web socket simple client."""
import asyncio
import websockets

async def hello():
    username = "foo"
    password = "bar"
    async with websockets.connect(f"ws://{username}:{password}@localhost:4242") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello())