import json

from . import state

def broadcast(message):
    payload = message if isinstance(message, str) else json.dumps(message)

    dead_clients = []

    for client in list(state.clients):
        if not client["alive"]:
            dead_clients.append(client)
            continue

        client["pending"] = payload
        client["event"].set()

    for client in dead_clients:
        if client in state.clients:
            state.clients.remove(client)

def publish_state():
    broadcast(state.get_state_data())

def publish_radar_data(angles, distances, increment):
    broadcast(
        {
            "type": "radarData",
            "angles": angles,
            "distances": distances,
            "increment": increment,
        }
    )

def publish_reading(angle, distance, increment):
    state.batch.append({"angle": angle, "distance": distance})

    if len(state.batch) >= state.BATCH_SIZE:
        flush_radar_data(increment)

def flush_radar_data(increment):
    if not state.batch:
        return

    angles = [reading["angle"] for reading in state.batch]
    distances = [reading["distance"] for reading in state.batch]
    publish_radar_data(angles, distances, increment)
    state.batch = []
