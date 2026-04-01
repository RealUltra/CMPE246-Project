BATCH_SIZE = 5

clients = []
batch = []

paused = False
buzzer_active = True
distance_threshold = 20
last_move_to_angle = None


def get_state_data():
    return {
        "type": "stateData",
        "paused": paused,
        "buzzerState": buzzer_active,
        "distanceThreshold": distance_threshold,
    }


def set_paused(value):
    global paused
    paused = bool(value)


def is_paused():
    return paused


def set_buzzer_active(value):
    global buzzer_active
    buzzer_active = bool(value)


def is_buzzer_active():
    return buzzer_active


def set_distance_threshold(value):
    global distance_threshold
    distance_threshold = int(value)


def get_distance_threshold():
    return distance_threshold


def set_move_to_angle(angle):
    global last_move_to_angle
    last_move_to_angle = int(angle)


def pop_move_to_angle():
    global last_move_to_angle
    angle = last_move_to_angle
    last_move_to_angle = None
    return angle
