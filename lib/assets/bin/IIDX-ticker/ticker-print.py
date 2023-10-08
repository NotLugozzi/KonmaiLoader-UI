# this code requires the tickerhook dll to be injected into game. it will print out the current ticker text and that's pretty much it.

import asyncio
import websockets

address = "localhost"

async def connect():
    uri = f"ws://{address}:10573"

    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                message = message.strip().upper()
                print(message)
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                await asyncio.sleep(1)
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())
