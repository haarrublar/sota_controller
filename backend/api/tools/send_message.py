import asyncio
import json
import websockets

async def send_test_message():
    uri = "ws://127.0.0.1:8000/ws/chat/"
    
    async with websockets.connect(uri) as websocket:
        payload = {"message": "Hello from Python script!"}
        await websocket.send(json.dumps(payload))
        print(f"Sent: {payload}")

        # Wait to receive the broadcasted message back
        response = await websocket.recv()
        print(f"Received back from broadcast: {response}")

if __name__ == "__main__":
    asyncio.run(send_test_message())