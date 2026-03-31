from gpiozero import AngularServo
from time import sleep

class ServoController:
    def __init__(self, gpio_pin, min_angle=0, max_angle=180):
        self._gpio_pin = gpio_pin
        self._MIN_ANGLE = min_angle
        self._MAX_ANGLE = max_angle
        self._current_angle = 0
        self.servo = None
        self.initialize()

    def initialize(self):
        self.servo = AngularServo(self._gpio_pin, min_angle=self._MIN_ANGLE, max_angle=self._MAX_ANGLE)
        self.rotate_to(0)

    def rotate_to(self, angle):
        if self._MIN_ANGLE <= angle <= self._MAX_ANGLE:
            self._current_angle = angle
            self.servo.angle = angle
            sleep(0.05)
        else:
            print(f"Angle {angle} is out of bounds.")
            
    @property
    def current_angle(self):
        return self._current_angle