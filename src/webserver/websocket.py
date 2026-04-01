import json
from threading import Event, Thread

from . import state
from .app import sock
from .socketio import publish_state


def client_sender(client):
    while client["alive"]:
        client["event"].wait()
        client["event"].clear()

        if not client["alive"]:
            break

        payload = client["pending"]
        client["pending"] = None

        if payload is None:
            continue

        try:
            client["ws"].send(payload)
        except Exception:
            client["alive"] = False
            if client in state.clients:
                state.clients.remove(client)
            break


@sock.route("/ws")
def websocket(ws):
    client = {
        "ws": ws,
        "pending": None,
        "event": Event(),
        "alive": True,
    }

    state.clients.append(client)
    Thread(target=client_sender, args=(client,), daemon=True).start()

    try:
        while True:
            message = ws.receive()

            if message is None:
                break

            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                continue

            if not isinstance(data, dict):
                continue

            message_type = data.get("type")

            if message_type == "setPause":
                state.set_paused(data.get("value"))
                publish_state()
            elif message_type == "moveTo":
                state.set_move_to_angle(data.get("angle"))
            elif message_type == "setBuzzerState":
                state.set_buzzer_active(data.get("active"))
                publish_state()
            elif message_type == "init":
                ws.send(json.dumps(state.get_state_data()))
            elif message_type == "setDistanceThreshold":
                state.set_distance_threshold(data.get("distance"))
                publish_state()
    finally:
        client["alive"] = False
        client["event"].set()
        if client in state.clients:
            state.clients.remove(client)
