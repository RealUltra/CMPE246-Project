const RADAR_PART_DISTANCE = 10;
const NUM_LINES = 5;
const MAX_DISTANCE = 80;
const SCANNER_SIZE = 30;

let radarWidth;
const obstacles = {}; // angle : distance
let angle = 180;
let increment = -1;
let distanceThreshold = 20;

function setup() {
  createCanvas(windowWidth, windowHeight / 2);
  radarWidth = min(width, height * 2) * 0.8;

  /*
  for (let a = 0; a <= 180; a++) {
    obstacles[a] = Math.random() * MAX_DISTANCE * 2 + MAX_DISTANCE / 2;
  }
  */

  setupComponents();
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight / 2);
  radarWidth = min(width, height * 2) * 0.8;
}

function setupComponents() {
  const pauseButton = document.getElementById("pauseButton");
  pauseButton.onclick = togglePause;

  const muteButton = document.getElementById("muteButton");
  muteButton.onclick = toggleMute;

  const dangerZoneInput = document.getElementById("dangerZoneInput");
  dangerZoneInput.addEventListener("input", function () {
    dangerZoneSlider.value = dangerZoneInput.value;
    onDangerZoneChanged();
  });
  dangerZoneInput.max = MAX_DISTANCE;

  const dangerZoneSlider = document.getElementById("dangerZoneSlider");
  dangerZoneSlider.addEventListener("input", function () {
    dangerZoneInput.value = dangerZoneSlider.value;
    onDangerZoneChanged();
  });
  dangerZoneSlider.max = MAX_DISTANCE;

  const updateDangerZoneButton = document.getElementById(
    "updateDangerZoneButton"
  );
  updateDangerZoneButton.onclick = updateDangerZonePressed;

  const cancelDangerZoneButton = document.getElementById(
    "cancelDangerZoneButton"
  );
  cancelDangerZoneButton.onclick = cancelDangerZonePressed;
}

function draw() {
  background(0);

  translate(width / 2, height - 1);

  if (mouseIsPressed) {
    const a = calculateAngle(mouseX, mouseY);

    if (a !== -1) {
      angle = a;
      sendMessage({ type: "moveTo", angle });
    }
  }

  noFill();

  drawRadar();
  drawScanner();
  drawDangerZone();
  drawInfo();

  /*
  angle += increment;

  if (angle >= 180 || angle <= 0) {
    increment *= -1;
  }
    */
}

function drawRadar() {
  // Draw Circles
  stroke(0, 255, 0);
  strokeWeight(2);

  const numCircles = MAX_DISTANCE / RADAR_PART_DISTANCE;

  for (let i = 0; i < numCircles; i++) {
    const circleWidth = (radarWidth / numCircles) * (i + 1);
    circle(0, 0, circleWidth);
  }

  // Draw Lines
  line(-width / 2, 0, width / 2, 0);

  const lineLength = radarWidth * 0.55;

  for (let i = 0; i < NUM_LINES; i++) {
    const angle = (-PI / (NUM_LINES + 1)) * (i + 1);
    const x = cos(angle) * lineLength;
    const y = sin(angle) * lineLength;
    line(0, 0, x, y);
  }
}

function drawScanner() {
  const length = radarWidth * 0.55;

  for (let i = 0; i < SCANNER_SIZE; i++) {
    const a =
      increment > 0
        ? max(angle, SCANNER_SIZE) - i
        : min(angle, 180 - SCANNER_SIZE) + i;

    const x = cos(radians(360 - a)) * length;
    const y = sin(radians(360 - a)) * length;

    strokeWeight(angle === a ? 2 : 1);
    stroke(0, 255, 0);
    line(0, 0, x, y);

    drawObstacle(a);
  }
}

function drawObstacle(angle) {
  const circleRadius = radarWidth / 2;

  const distance = obstacles[angle];

  if (distance && distance != 0.0 && distance < MAX_DISTANCE) {
    if (distance < distanceThreshold) {
      stroke(255, 0, 0);
    } else {
      stroke(255, 255, 0);
    }

    const obstacleLength = (distance / MAX_DISTANCE) * circleRadius;
    const x = cos(radians(360 - angle)) * obstacleLength;
    const y = sin(radians(360 - angle)) * obstacleLength;
    const topX = cos(radians(360 - angle)) * circleRadius;
    const topY = sin(radians(360 - angle)) * circleRadius;

    line(topX, topY, x, y);
  }
}

function drawDangerZone() {
  const dangerZoneDiameter = (distanceThreshold / MAX_DISTANCE) * radarWidth;

  strokeWeight(3);
  stroke(255, 0, 0);
  circle(0, 0, dangerZoneDiameter);

  const dangerZoneValue = getDangerZone();

  if (dangerZoneValue !== null && dangerZoneValue !== distanceThreshold) {
    const diameter = (dangerZoneValue / MAX_DISTANCE) * radarWidth;
    strokeWeight(2);
    stroke(0, 255, 255);
    circle(0, 0, diameter);
  }
}

function drawInfo() {
  noStroke();
  fill(255, 255, 255);

  textSize(16);
  textAlign(RIGHT, TOP);
  text(`Angle: ${180 - angle}°`, width / 2 - 30, -height + 30);

  let distance = obstacles[angle] ?? null;
  distance = distance !== 0 ? distance : null;

  if (distance) {
    distance = Math.round(distance * 100) / 100;
  }

  textAlign(RIGHT, TOP);
  text(`Distance: ${distance ?? "?"} cm`, width / 2 - 30, -height + 60);
}

function calculateAngle(x, y) {
  const xDiff = width / 2 - x;
  const yDiff = height - y;

  if (yDiff < 0) {
    return -1;
  }

  let a = degrees(atan2(yDiff, xDiff));

  return int(180 - a);
}

function setDistance(distance) {
  obstacles[angle] = distance;
}

function togglePause() {
  setPaused(!isPaused());

  sendMessage({ type: "setPause", value: isPaused() });
}

function toggleMute() {
  setMuted(!isMuted());

  sendMessage({ type: "setBuzzerState", active: !isMuted() });
}

function isPaused() {
  const pauseButton = document.getElementById("pauseButton");
  return pauseButton.classList.contains("unpauseButton");
}

function setPaused(value) {
  if (value === isPaused()) {
    // Already that value.
    return;
  }

  // Visual changes
  const pauseButton = document.getElementById("pauseButton");

  if (value) {
    pauseButton.textContent = "Unpause";
    pauseButton.classList.remove("pauseButton");
    pauseButton.classList.add("unpauseButton");
  } else {
    pauseButton.textContent = "Pause";
    pauseButton.classList.remove("unpauseButton");
    pauseButton.classList.add("pauseButton");
  }
}

function isMuted() {
  const muteButton = document.getElementById("muteButton");
  return muteButton.classList.contains("mutedButton");
}

function setMuted(value) {
  if (value === isMuted()) {
    // Already set to that.
    return;
  }

  // Visual changes
  const muteButton = document.getElementById("muteButton");

  const mutedSvg = document.getElementById("muted-svg");
  const unmutedSvg = document.getElementById("unmuted-svg");

  if (!value) {
    // Set to Unmuted
    muteButton.classList.remove("mutedButton");
    muteButton.classList.add("unmutedButton");

    unmutedSvg.classList.remove("hidden");
    mutedSvg.classList.add("hidden");
  } else {
    muteButton.classList.remove("unmutedButton");
    muteButton.classList.add("mutedButton");

    mutedSvg.classList.remove("hidden");
    unmutedSvg.classList.add("hidden");
  }
}

function enableDangerZoneButton() {
  const button = document.getElementById("updateDangerZoneButton");
  button.disabled = false;
}

function disableDangerZoneButton() {
  const button = document.getElementById("updateDangerZoneButton");
  button.disabled = true;
}

function getDangerZone() {
  const dangerZoneInput = document.getElementById("dangerZoneInput");

  const value = dangerZoneInput.value;

  if (value === "") {
    return null;
  }

  return max(min(int(value), MAX_DISTANCE), 5);
}

function setDangerZone(distance) {
  const dangerZoneInput = document.getElementById("dangerZoneInput");
  const dangerZoneSlider = document.getElementById("dangerZoneSlider");

  dangerZoneInput.value = distance;
  dangerZoneSlider.value = distance;

  onDangerZoneChanged();
}

function onDangerZoneChanged() {
  const dangerZoneValue = getDangerZone();

  if (dangerZoneValue !== null && dangerZoneValue !== distanceThreshold) {
    enableDangerZoneButton();
  } else {
    disableDangerZoneButton();
  }
}

function updateDangerZonePressed(event) {
  distanceThreshold = getDangerZone();
  disableDangerZoneButton();

  sendMessage({
    type: "setDistanceThreshold",
    distance: distanceThreshold,
  });
}

function cancelDangerZonePressed(event) {
  setDangerZone(distanceThreshold);
  disableDangerZoneButton();
}
