# CMPE 246 Project: Ultrasonic Radar

This project builds an ultrasonic radar using an HC-SR04 time-of-flight (ToF) sensor mounted on a micro servo to create a 2D map of nearby objects.
At each angle step, a Raspberry Pi measures distance and streams angle-distance data to a lightweight web UI (Flask + JavaScript/p5.js) for real-time radar visualization.

## Index

- [Team](#team)
  - [Rameez Baig](#rameez-baig)
  - [Chigoziri Okpanku](#chigoziri-okpanku)
  - [Joshua Seo](#joshua-seo)
  - [Rania Atmani Garmavich](#rania-atmani-garmavich)
  - [_Shared Responsibilities_](#shared-responsibilities)
- [Timeline](#timeline)
  - [Week 6-7: Project Planning & Initial Design](#week-6-7-project-planning--initial-design)
  - [Week 8: Hardware Setup](#week-8-hardware-setup)
  - [Week 9: Embedded Software Development](#week-9-embedded-software-development)
  - [Week 10: Wireless Communication & UI Development](#week-10-wireless-communication--ui-development)
  - [Week 11-12: Refinement & Preparation](#week-11-12-refinement--preparation)
  - [Weeks 13-14: Presentation & Evaluation](#weeks-13-14-presentation--evaluation)
- [Hardware](#hardware)
- [Software](#software)

## Team

### Rameez Baig

#### Roles:

- **Wireless Communication Engineer**
- **UI & Integration Lead**

#### Responsibilities:

- Set up the Raspberry Pi as a permanent AP.
- Host a web server on the Raspberry Pi.
- Build an appealing visual display for the radar.
- Map the data from the sensors to the UI.
- Host the UI on the web server.

### Chigoziri Okpanku

#### Role: Hardware Lead

#### Responsibilities:

- Integrate the ultrasonic sensor & servo.
- Handle GPIO pin consideration & power considerations.
- Test hardware and troubleshoot issues.
- Produce a circuit diagram.

### Joshua Seo

#### Role: Embedded Software Developer

#### Responsibilities:

- Design the core software to utilize the ultrasonic sensor & servo using object-oriented principles.
- Coordinate the ultrasonic sensor with the servo.
- Implement classes such as:
  - **UltrasonicSensor**
  - **ServoController**
- Optimize timing and mitigate delay.
- Prepare UML diagrams showing class relationships.

### Rania Atmani Garmavich

#### Role: Writing & Marketing Lead

#### Responsibilities:

- Handle the bulk of the writing portions e.g. proposal documents, presentations, etc.
- Maintain a social media presence showcasing our product.
- Create engaging videos for engagement on Instagram.

### Shared Responsibilities:

- **Documentation & Reporting:** All members must maintain a consistent work log.
- **Testing & Debugging:** All members are responsible for testing & debugging their work.
- **Reflection Writing:** All members must write individual reflections at the beginning and end of the project timeline.
- **Version Control with GitHub:** All members will use Git & GitHub for accurate version management and contribution tracking.

## Timeline

### Week 6-7: Project Planning & Initial Design

- Finalize project scope & requirements.
- Assign team roles & responsibilities.
- Select hardware components and software libraries.
- Choose a software framework for the UI.
- Draft initial circuit diagrams.
- Create preliminary UML Diagrams.

### Week 8: Hardware Setup

- Wire and test the ultrasonic sensor & servo motor together.
- Configure GPIO pins and satisfy power requirements.
- Implement basic servo movement software & ultrasonic sensor distance calculation software.

### Week 9: Embedded Software Development

- Implement core software using object-oriented design.
- Develop classes such as:
  - **UltrasonicSensor**
  - **ServoController**
- Coordinate sensor readings with servo rotation.
- Optimize timings & reduce measurement delays.
- Update UML diagrams to reflect final class structure.

### Week 10: Wireless Communication & UI Development

- Configure Raspberry Pi as a wireless access point.
- Set up a web server on the Raspberry Pi.
- Define data format (angle-distance pairs).
- Transmit radar data from the device to a client.
- Develop radar visualization interface.
- Map incoming data to visual display.

### Week 11-12: Refinement & Preparation

- Final debugging and performance tuning
- Validate reliability of hardware connections.
- Finalize diagrams, screenshots & demo materials.
- Prepare reflection content.

### Weeks 13-14: Presentation & Evaluation

- Deliver project presentation and live demonstration.
- Present design decisions, results & findings.
- Discuss challenges, limitations and lessons learned.

## Hardware

#### Raspberry Pi 4

- Main control unit of the system.
- Interfaces with the ultrasonic sensor & servo motor.
- Supports web server hosting for data transmission & visualization.

#### Ultrasonic Distance Sensor (HC-SR04 or equivalent)

- Used to measure the distance of objects by emitting ultrasonic pulses and calculating the distance based on echo return time.
- Suitable for low-to-medium-range distance measurement.

#### Micro Servo Motor (SG90 or MG90S)

- Used to rotate the ultrasonic sensor across a defined angular range.
- Enables scanning a wider area and allows for radar visualization by associating specific angles with distance measurements.

#### Supporting Components

- Breadboard
- Jumper Wires
- External Power Supply
- Mounting Hardware

## Software

#### Python

- Used for embedded software development on the Raspberry Pi.
- Enables rapid prototyping, easy-to-read object-oriented code, and easy integration with GPIO and networking libraries.

#### GPIO Control Libraries (gpiozero)

- Used to control the servo motor movement and the utilize the ultrasonic sensor.

#### Web Server Framework (Flask)

- Used to easily host a web server for the radar visualization interface between the Raspberry Pi and connected clients.

#### UI Framework (HTML, CSS, Javascript, p5.js)

- Used to create the radar-style visualization interface that displays distance and angle data in real-time.


