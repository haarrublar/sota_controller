import sys
from pathlib import Path
import pygame
import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))
from SOTA.sota_controller.backend.api.controllerDriver.xbox import XboxController



controller = XboxController()
clock = pygame.time.Clock()

DJANGO_URL = "http://localhost:8000/api/controller-events/"

last_axes = None

while True:
    controller.poll()
    axes = controller.get_axes()


    if axes != last_axes:
        active = {k: v for k, v in axes.items() if v not in (0.0, False)}
        if active:
            print(active)
            try:
                requests.post(DJANGO_URL, json={"type": "axes", "data": active}, timeout=0.5)
            except requests.exceptions.RequestException as e:
                print("Failed to send:", e)
        last_axes = axes

    clock.tick(60)