import os
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

from ultrasonic_sensor import UltrasonicSensor
from servo_controller import ServoController
from radar import Radar

TRIGGER_PIN = 18
ECHO_PIN = 12
SERVO_PIN = 19
BUZZER_PIN = 23

def main():
    sensor = UltrasonicSensor(trigger_pin=TRIGGER_PIN, echo_pin=ECHO_PIN)
    servo = ServoController(gpio_pin=SERVO_PIN)
    radar = Radar(ultrasonic_sensor=sensor, servo_controller=servo, buzzer_pin=BUZZER_PIN)

    print("Radar System Turned On.")
    print("Commands: 'scan' to start, 'pause' to toggle pause, 'exit' to quit.")
    
    while True:
        user_choice = input("\nEnter command: ").strip().lower()
        
        if user_choice == "scan":
            radar.update()
        elif user_choice == "pause":
            radar.toggle_pause()
        elif user_choice == "exit":
            print("Shutting down...")
            radar.reset()
            break
        else:
            print("Unknown command. Type 'scan', 'pause', or 'exit'.")

if __name__ == "__main__":
    main()