from gpiozero import DistanceSensor, AngularServo, Buzzer
from time import sleep

Trigger=18, Echo=12, Servo=19, Buzzer_pin=23

sensor = DistanceSensor(echo=12, trigger=18)
servo = AngularServo(19, min_angle=0, max_angle=180)
buzzer = Buzzer(Buzzer_pin)
triggerdist = 20

servo.angle = 0

def perform_radar_scan():
    print("Scanning Started")
    
    for angle in range(0, 181):
        servo.angle = angle
        check_and_beep(triggerdist)
        sleep(0.05)
    
    for angle in range(180, -1, -1):
        servo.angle = angle
        check_and_beep(triggerdist)
        sleep(0.05)
        
    print("Scan Complete")
    servo.angle = 0 

def check_and_beep(triggerdist):
    dist_cm = sensor.distance * 100
    if dist_cm < triggerdist:
        print(f"Object detected is {dist_cm:.1f} cm away“)
        buzzer.on()
        sleep(0.1)
        buzzer.off()

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


