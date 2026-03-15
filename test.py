import asyncio, websockets, json

async def test():
    async with websockets.connect("ws://localhost:8088/ws/test-session1") as ws:
        await ws.send("Josh Allen,QB,Wyoming")
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=30)
            print(response)
        except asyncio.TimeoutError:
            print("No response received within 30 seconds")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}")

asyncio.run(test())
