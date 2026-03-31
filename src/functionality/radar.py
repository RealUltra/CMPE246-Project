from distance_reading import DistanceReading
from gpiozero import Buzzer
from time import sleep

class Radar:
    def __init__(self, ultrasonic_sensor, servo_controller, buzzer_pin):
        self._ultrasonic_sensor = ultrasonic_sensor
        self._servo = servo_controller
        self._is_paused = False
        self.buzzer = Buzzer(buzzer_pin)
        self.triggerdist = 20
        self.scantime = 0.1

    def reset(self):
        self._is_paused = False
        self._servo.rotate_to(0)

    def toggle_pause(self):
        self._is_paused = not self._is_paused
        state = "paused" if self._is_paused else "resumed"
        print(f"Radar {state}.")

    def update(self):
        #Performs a full sweep
        print("Scanning Started")
        
        # Sweep forward
        for angle in range(0, 181):
            if self._is_paused:
                return
            self._servo.rotate_to(angle)
            self._check_and_beep()
            
        # Sweep backward
        for angle in range(180, -1, -1):
            if self._is_paused:
                return
            self._servo.rotate_to(angle)
            self._check_and_beep()
            
        print("Scan Complete")
        self.reset()

    def _check_and_beep(self):
        dist_cm = self._ultrasonic_sensor.measure_distance()
        reading = DistanceReading(self._servo.current_angle, dist_cm)
        
        if reading.distance < self.triggerdist:
            print(f"Object detected at {reading.angle} deg: {reading.distance:.1f} cm away")
            temp = reading.distance / self.triggerdist
            ont = self.scantime * temp
            offt = self.scantime - ont

            self.buzzer.on()
            sleep(max(0, ont))
            self.buzzer.off()
            sleep(max(0, offt))