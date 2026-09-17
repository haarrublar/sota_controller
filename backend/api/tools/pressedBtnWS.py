import asyncio
import json
import pygame
import sys
from pathlib import Path
import websockets

sys.path.append(str(Path(__file__).resolve().parent.parent))
from controllerDriver.xbox import XboxController

async def main():
    uri = "ws://127.0.0.1:8000/ws/controller-buttons/"
    controller = XboxController()
    clock = pygame.time.Clock()

    async with websockets.connect(uri) as ws:
        while True:
            controller.poll()
            pressed = controller.get_pressed()

            if pressed:
                await ws.send(json.dumps({"type": "button", "name": pressed}))
                
                response = await ws.recv()
                print(f"{response}")

            await asyncio.sleep(1 / 60)  

if __name__ == "__main__":
    asyncio.run(main())