from gpiozero import DistanceSensor

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self._trigger_pin = trigger_pin
        self._echo_pin = echo_pin
        self.sensor = None
        self.initialize()

    def initialize(self):
        self.sensor = DistanceSensor(echo=self._echo_pin, trigger=self._trigger_pin)

    def measure_distance(self):
        #Distance is in cm
        return self.sensor.distance * 100