from controller import XboxController
import pygame
import requests
from time import time

controller = XboxController()
clock = pygame.time.Clock()

DJANGO_URL = "http://localhost:8000/api"

recording = False
recording_frames = []
recording_start_time = None

while True:
    controller.poll()
    pressed = controller.get_pressed()
    axes = controller.get_axes()

    if pressed == "START" and not recording:
        recording = True
        recording_frames = []
        recording_start_time = time()
        print("Recording started (holding START)...")

    elif controller.is_released("START") and recording:
        recording = False
        duration_ms = int((time() - recording_start_time) * 1000)
        
        try:
            requests.post(
                f"{DJANGO_URL}/recordings/",
                json={
                    "name": "Xbox Recording",
                    "frames": recording_frames,
                    "duration_ms": duration_ms,
                    "frame_rate": 60,
                },
                timeout=2
            )
            print(f"Recording saved: {len(recording_frames)} frames")
        except requests.exceptions.RequestException as e:
            print("Failed to save recording:", e)

    elif pressed and not recording:
        try:
            requests.post(
                f"{DJANGO_URL}/controller-events/",
                json={"type": "button", "name": pressed},
                timeout=0.5
            )
        except requests.exceptions.RequestException:
            pass

    if recording:
        frame = {"t": round(time() - recording_start_time, 4), **axes}
        if pressed and pressed != "START":
            frame["button"] = pressed
        recording_frames.append(frame)

    clock.tick(60)