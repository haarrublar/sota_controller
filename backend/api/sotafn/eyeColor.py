import asyncio
import json

import websockets

from sota_thinclient.connection_manager import ConnectionManager
from sota_thinclient.pose import LedID, SotaState

WS_URL = "ws://127.0.0.1:8000/ws/controller-buttons/"

SOTA_IP = "10.151.63.79"
HTTP_PORT = "8080"


def set_eye_color(sota, color):

    new_state = SotaState()
    new_state.leds[LedID.LEFT_EYE] = color
    new_state.leds[LedID.RIGHT_EYE] = color
    sota.pose.send_command(new_state,msec=1000)



async def main():

    print("Connecting to Sota...")
    sota = ConnectionManager(SOTA_IP,HTTP_PORT)

    try:
        print(f"Connecting to Sota at {SOTA_IP}:{HTTP_PORT}...")

        await asyncio.to_thread(sota.pose.enable)

        print("Sota connected and enabled.")
        print(f"Connecting to WebSocket: {WS_URL}")

        async with websockets.connect(WS_URL) as ws:

            print("WebSocket connected.")
            print("Waiting for color commands...\n")

            while True:

                try:
                    message = await ws.recv()
                    print("Received:", message)
                    data = json.loads(message)

                    if data.get("action") != "SELECT_COLOR":
                        continue
                    raw_hex = data.get("color",{}).get("hex","")

                    if not raw_hex:
                        print("No color received.")
                        continue

                    eye_color = f"#{raw_hex.lstrip('#')}"

                    print(f"SELECT_COLOR received: {eye_color}")

                    await asyncio.to_thread(
                        set_eye_color,
                        sota,
                        eye_color
                    )

                except json.JSONDecodeError:
                    print(
                        "Received invalid JSON:",
                        message
                    )

                except websockets.ConnectionClosed:
                    print(
                        "WebSocket connection closed."
                    )
                    break

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        print("Disabling Sota...")

        try:
            await asyncio.to_thread(
                sota.pose.disable
            )
        except Exception as e:
            print(
                f"Error disabling Sota: {e}"
            )

        print("Program stopped.")


if __name__ == "__main__":
    asyncio.run(main())
