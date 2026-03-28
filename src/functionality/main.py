import os 
os.environ["GPIOZEREO_PIN_FACTORY"] = "pigpio"

from gpiozero import DistanceSensor, AngularServo, Buzzer
from time import sleep

Trigger=18, Echo=12, Servo=19, Buzzer_pin=23

sensor = DistanceSensor(echo=12, trigger=18)
servo = AngularServo(19, min_angle=0, max_angle=180)
buzzer = Buzzer(Buzzer_pin)
triggerdist = 20
scantime = 0.1
servo.angle = 0

def perform_radar_scan():
    print("Scanning Started")
    
    for angle in range(0, 181):
        servo.angle = angle
        check_and_beep(triggerdist,scantime)
        sleep(0.05)
    
    for angle in range(180, -1, -1):
        servo.angle = angle
        check_and_beep(triggerdist,scantime)
        sleep(0.05)
        
    print("Scan Complete")
    servo.angle = 0 

def check_and_beep(triggerdist, scantime):
    dist_cm = sensor.distance * 100
    if dist_cm < triggerdist:
        print(f"Object detected is {dist_cm:.1f} cm away")
        temp = dist_cm/triggerdist
        ont = scantime*temp
        offt = scantime - ont


        buzzer.on()
        sleep(ont)
        buzzer.off()
        sleep(offt)

        #change buzzer so it beeps more based off distance. 

def main():
    print("Radar System Turned On.")
    print("Commands: 'scan' to start, 'exit' to quit.")
    
    while True:
        user_choice = input("\nEnter command: ").strip().lower()
        
        if user_choice == "scan":
            perform_radar_scan()
        elif user_choice == "exit":
            print("Shutting down")
            break
        else:
            print("Unknown command. Type 'scan' to begin.")

if __name__ == "__main__":
    main()


