from .distance_reading import DistanceReading
from gpiozero import Buzzer
from time import time

class Radar:
    def __init__(self, ultrasonic_sensor, servo_controller, buzzer_pin):
        self._ultrasonic_sensor = ultrasonic_sensor
        self._servo = servo_controller
        self._is_paused = False
        self._increment = 1

        self.buzzer = Buzzer(buzzer_pin)
        self.triggerdist = 20
        self.buzzer_active = True
        self._buzzing = False
        self._buzz_deadline = 0.0

    def reset(self):
        self._is_paused = False
        self._increment = 1
        self._servo.rotate_to(0)
        self.buzzer.off()
        self._buzzing = False
        self._buzz_deadline = 0.0

    def set_paused(self, is_paused):
        if is_paused == self._is_paused:
            return

        self._is_paused = is_paused
        state = "paused" if self._is_paused else "resumed"
        print(f"Radar {state}.")

    def is_paused(self):
        return self._is_paused

    def update(self):
        min_angle = self._servo.min_angle
        max_angle = self._servo.max_angle

        if not self._is_paused:
            next_angle = self._servo.current_angle + self._increment

            if next_angle > max_angle or next_angle < min_angle:
                self._increment *= -1
                next_angle = self._servo.current_angle + self._increment

            self._servo.rotate_to(next_angle)

        dist_cm = self._ultrasonic_sensor.measure_distance()

        self.beep(dist_cm)

        return DistanceReading(self._servo.current_angle, dist_cm)

    @property
    def increment(self):
        return self._increment

    def beep(self, distance):
        '''
        ---======= Distance-Relative Beeping =======---

        This buzzer logic uses timestamps instead of sleep().
        That is important because sleep() would pause the whole radar loop and
        slow down the servo. Here, beep() only checks the clock and decides
        whether the buzzer should change state yet.

        _buzz_deadline:
        This stores the exact future time when the buzzer should change state
        next.
        Example:
        - if the buzzer just turned ON, _buzz_deadline is the time when it
          should turn OFF
        - if the buzzer just turned OFF, _buzz_deadline is the time when it
          should turn ON again

        So when the code does:
            if now < self._buzz_deadline:
                return
        it means:
        "it is not time to change the buzzer yet, so leave it alone."

        cycle_time:
        This is the total time for one complete beep cycle.
        A complete cycle means:
        - the buzzer turns ON
        - it stays ON for on_time
        - it then turns OFF
        - it stays OFF until it is time to turn ON again

        So cycle_time is the time from:
        - one ON event
        to
        - the next ON event

        In other words:
            cycle_time = on_time + off_time

        Distance controls cycle_time:
        - closer object -> smaller cycle_time -> the ON events happen more often
        - farther object -> larger cycle_time -> the ON events happen less often

        How cycle_time is calculated:
            cycle_time = 0.04 + (distance / self.triggerdist * 0.31)

        Step by step:
        - distance / self.triggerdist gives a value between 0 and 1
          - 0 means the object is extremely close
          - 1 means the object is right at the trigger distance
        - that value is then multiplied by 0.31
          - so it produces something between 0 and 0.31
        - then 0.04 is added
          - so the final cycle_time is between 0.04 and 0.35 seconds

        That means:
        - very close object -> cycle_time near 0.04 seconds
        - object near the trigger distance -> cycle_time near 0.35 seconds

        So the constants 0.04 and 0.31 simply define the minimum and maximum
        speed of the beeping.

        on_time:
        This is how long the buzzer stays ON during one cycle.
        The OFF time is the rest of the cycle:
            off_time = cycle_time - on_time

        How on_time is calculated:
            on_time = max(0.01, cycle_time * 0.3)

        Step by step:
        - cycle_time * 0.3 means the buzzer stays ON for about 30% of the full cycle
        - max(0.01, ...) means the ON time is never allowed to go below 0.01 seconds

        The minimum is there so that even when the cycle gets very short, the
        buzzer still stays ON long enough to produce a noticeable beep.
        We don't want the buzzer sound to be constant.

        General flow:
        1. If the buzzer is disabled, or the object is outside the trigger
           distance, turn the buzzer OFF and clear the timing state.
        2. If the current time has not reached _buzz_deadline yet, return
           immediately and do nothing.
        3. If the deadline has been reached:
           - if the buzzer is currently OFF, turn it ON and set the next
             deadline to now + on_time
           - if the buzzer is currently ON, turn it OFF and set the next
             deadline to now + off_time

        So the buzzer gets more urgent as objects get closer, but the radar
        loop stays smooth because this function never blocks.

        '''

        if not self.buzzer_active or distance == 0.0 or distance >= self.triggerdist:
            self.buzzer.off()
            self._buzzing = False
            self._buzz_deadline = 0.0
            return

        now = time()

        if now < self._buzz_deadline:
            return

        cycle_time = 0.04 + (distance / self.triggerdist * 0.31)
        on_time = max(0.01, cycle_time * 0.3)

        if not self._buzzing:
            self.buzzer.on()
            self._buzzing = True
            self._buzz_deadline = now + on_time
        else:
            self.buzzer.off()
            self._buzzing = False
            self._buzz_deadline = now + (cycle_time - on_time)
