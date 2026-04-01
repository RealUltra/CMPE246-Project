from gpiozero import AngularServo
from time import sleep

class ServoController:
    def __init__(self, gpio_pin, min_angle=0, max_angle=180):
        self._gpio_pin = gpio_pin
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._current_angle = 0
        self.servo = None
        self.initialize()

    def initialize(self):
        self.servo = AngularServo(self._gpio_pin, min_angle=self._min_angle, max_angle=self._max_angle)
        self.rotate_to(0)

    def rotate_to(self, angle):
        if angle == self._current_angle:
            return

        if angle >= self._min_angle and angle <= self._max_angle:
            self._current_angle = angle
            self.servo.angle = angle
        else:
            print(f"Angle {angle} is out of bounds.")
            
    @property
    def current_angle(self):
        return self._current_angle
    
    @property
    def min_angle(self):
        return self._min_angle
    
    @property
    def max_angle(self):
        return self._max_angle