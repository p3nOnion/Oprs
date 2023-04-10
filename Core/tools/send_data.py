import asyncio
import json

import websockets
import sys

# Lấy tất cả các arguments truyền vào script
args = sys.argv

# In ra tất cả các arguments
print(args)

async def connect():
    uri = 'ws://'+args[1]+'/ws/message/0'
    print(uri)
    async with websockets.connect(uri) as websocket:
        message = {"message":args[2]}
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print(f"Received message from server: {response}")

async def main():
    await connect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())