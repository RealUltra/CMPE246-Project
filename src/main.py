import os
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

from time import sleep

from functionality.ultrasonic_sensor import UltrasonicSensor
from functionality.servo_controller import ServoController
from functionality.radar import Radar

from webserver import *

TRIGGER_PIN = 18
ECHO_PIN = 12
SERVO_PIN = 19
BUZZER_PIN = 23

def main():
    sensor = UltrasonicSensor(trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN)
    servo = ServoController(gpio_pin=SERVO_PIN)
    radar = Radar(ultrasonic_sensor=sensor, servo_controller=servo, buzzer_pin=BUZZER_PIN)

    start_server()

    print("Radar System Turned On.")

    try:
        while True:
            radar.triggerdist = get_distance_threshold()
            radar.buzzer_active = is_buzzer_active()
            radar.set_paused(is_paused())

            move_to_angle = pop_move_to_angle()
            if move_to_angle is not None:
                servo.rotate_to(move_to_angle)

            reading = radar.update()
            if reading is not None:
                publish_reading(reading.angle, reading.distance, radar.increment)

            sleep(0.015)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        flush_radar_data(radar.increment)
        radar.reset()

if __name__ == "__main__":
    main()
