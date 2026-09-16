import pygame
import requests
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))
from controllerDriver.xbox import XboxController

controller = XboxController()
clock = pygame.time.Clock()

DJANGO_URL = "http://localhost:8000/api/controller-events/"

while True:
    controller.poll()
    pressed = controller.get_pressed()

    if pressed:
        print(f"{pressed} pressed")
        try:
            requests.post(DJANGO_URL, json={"type": "button", "name": pressed}, timeout=0.5)
        except requests.exceptions.RequestException as e:
            print("Failed to send event:", e)

    clock.tick(60)