let socket;
let initialized = false;
let reconnectTimeout = null;
let lastMessageTime = 0;

const RECONNECT_DELAY_MS = 2000;
const MESSAGE_TIMEOUT_MS = 3000;

window.addEventListener("load", onload);

function onload(event) {
  setInterval(checkSocketHealth, 1000);
  initWebSocket();
}

function initWebSocket() {
  if (reconnectTimeout !== null) {
    clearTimeout(reconnectTimeout);
    reconnectTimeout = null;
  }

  cleanupSocket();

  const ws = new WebSocket(`ws://${location.host}/ws`);
  socket = ws;
  ws.onopen = (event) => onOpen(event, ws);
  ws.onmessage = (event) => onMessage(event, ws);
  ws.onclose = (event) => onClose(event, ws);
  ws.onerror = (event) => onError(event, ws);
}

function cleanupSocket() {
  if (!socket) {
    return;
  }

  const oldSocket = socket;
  socket = null;

  oldSocket.onopen = null;
  oldSocket.onmessage = null;
  oldSocket.onclose = null;
  oldSocket.onerror = null;

  if (
    oldSocket.readyState === WebSocket.OPEN ||
    oldSocket.readyState === WebSocket.CONNECTING
  ) {
    try {
      oldSocket.close();
    } catch (e) {}
  }
}

function scheduleReconnect(delay = RECONNECT_DELAY_MS) {
  if (reconnectTimeout !== null) {
    return;
  }

  reconnectTimeout = setTimeout(() => {
    reconnectTimeout = null;
    initWebSocket();
  }, delay);
}

function checkSocketHealth() {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    return;
  }

  if (Date.now() - lastMessageTime > MESSAGE_TIMEOUT_MS) {
    cleanupSocket();
    scheduleReconnect(0);
  }
}

function sendMessage(data) {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    return false;
  }

  try {
    socket.send(JSON.stringify(data));
    return true;
  } catch (e) {
    cleanupSocket();
    scheduleReconnect(0);
    return false;
  }
}

function onOpen(event, ws) {
  if (socket !== ws) {
    return;
  }

  lastMessageTime = Date.now();
  sendMessage({ type: "init" });
}

function onMessage(event, ws) {
  if (socket !== ws) {
    return;
  }

  lastMessageTime = Date.now();

  let data;

  try {
    data = JSON.parse(event.data);
  } catch (e) {
    return;
  }

  const type = data.type;

  if (type === "radarData") {
    let angles = data.angles;
    let distances = data.distances;
    increment = data.increment;

    angle = increment > 0 ? Math.max(...angles) : Math.min(...angles);

    for (let i = 0; i < angles.length; i++) {
      obstacles[angles[i]] = distances[i];
    }
  } else if (type === "stateData") {
    setPaused(data.paused);
    setMuted(!data.buzzerState);

    const newThreshold = data.distanceThreshold;

    if (getDangerZone() === distanceThreshold || !initialized) {
      setDangerZone(newThreshold);
    }

    distanceThreshold = newThreshold;
    initialized = true;
  }
}

function onClose(event, ws) {
  if (socket !== ws) {
    return;
  }

  cleanupSocket();
  scheduleReconnect();
}

function onError(event, ws) {
  if (socket !== ws) {
    return;
  }

  cleanupSocket();
  scheduleReconnect();
}
