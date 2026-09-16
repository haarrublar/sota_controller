import pygame

class XboxController:

    BUTTONS = {
        "A": 0, "B": 1, "X": 2, "Y": 3,
        "LB": 4, "RB": 5, "BACK": 6, "START": 7,
        "L3": 8, "R3": 9, "GUIDE": 10, "SHARE": 11,
        "TRIM_FORWARD": 12, "TRIM_BACKWARD": 13,
        "TRIM_LEFT": 14, "TRIM_RIGHT": 15,
    }

    AXES = {
        "LEFT_X": 0, "LEFT_Y": 1,
        "RIGHT_X": 2, "RIGHT_Y": 3,
        "LT": 4, "RT": 5,
    }

    TRIGGER_THRESHOLD = 0.0  # midpoint if resting=-1.0, pressed=1.0 — adjust after checking real values

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self._prev_buttons = {name: False for name in self.BUTTONS}
        self._prev_triggers = {"LT": False, "RT": False}

    def poll(self):
        pygame.event.pump()

    def is_pressed(self, button_name):
        if button_name in self.BUTTONS:
            index = self.BUTTONS[button_name]
            current = bool(self.joystick.get_button(index))
            was_pressed = self._prev_buttons[button_name]
            self._prev_buttons[button_name] = current
            return current and not was_pressed

        if button_name in self._prev_triggers:
            index = self.AXES[button_name]
            value = self.joystick.get_axis(index)
            current = value > self.TRIGGER_THRESHOLD
            was_pressed = self._prev_triggers[button_name]
            self._prev_triggers[button_name] = current
            return current and not was_pressed

        raise ValueError(f"Unknown button/direction: {button_name}")

    def is_held(self, button_name):
        if button_name in self.BUTTONS:
            index = self.BUTTONS[button_name]
            return bool(self.joystick.get_button(index))

        if button_name in self._prev_triggers:
            index = self.AXES[button_name]
            return self.joystick.get_axis(index) > self.TRIGGER_THRESHOLD

        raise ValueError(f"Unknown button/direction: {button_name}")

    def is_released(self, button_name):
        if button_name in self.BUTTONS:
            index = self.BUTTONS[button_name]
            current = bool(self.joystick.get_button(index))
            was_pressed = self._prev_buttons[button_name]
            self._prev_buttons[button_name] = current
            return not current and was_pressed

        if button_name in self._prev_triggers:
            index = self.AXES[button_name]
            value = self.joystick.get_axis(index)
            current = value > self.TRIGGER_THRESHOLD
            was_pressed = self._prev_triggers[button_name]
            self._prev_triggers[button_name] = current
            return not current and was_pressed

        raise ValueError(f"Unknown button/direction: {button_name}")

    def get_pressed(self):
        for name in self.BUTTONS:
            if self.is_pressed(name):
                return name
        for name in self._prev_triggers:
            if self.is_pressed(name):
                return name
        return None

    def get_axis_value(self, axis_name):
        index = self.AXES[axis_name]
        return self.joystick.get_axis(index)
    
    def get_axes(self, deadzone=0.1):
        """Returns a single dict snapshot of all axis values for this frame."""
        snapshot = {}
        for name, index in self.AXES.items():
            value = self.joystick.get_axis(index)
            snapshot[name] = value if abs(value) > deadzone else 0.0
        return snapshot