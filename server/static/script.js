import { Room } from "./room.js";

const roomId = "testroom";

let room;
let highlighted;
let currentChallenge = "maze";
let autoStepTimer = null;

async function getChallenges() {
  const response = await fetch("/api/challenges");
  const challenges = await response.json();
  const select = document.querySelector("#challenge-dropdown");
  select.childNodes.forEach((child) => select.removeChild(child));
  challenges.forEach((challenge) => {
    const option = document.createElement("option");
    option.textContent = challenge;
    option.value = challenge;
    select.appendChild(option);
  });
  select.value = currentChallenge;
}

async function initRoom(challenge) {
  currentChallenge = challenge;
  clearInterval(autoStepTimer);
  autoStepTimer = null;
  await fetch(`/api/rooms/${roomId}?from_challenge=${challenge}`, {
    method: "PUT",
  });
  room = new Room(document.querySelector(".room-area"));
  highlighted = null;
  room.addEventListener("highlighted", ({ detail: { id } }) => {
    highlighted = id;
    update();
  });

  await update();
}

async function update() {
  const [roomData, entityData, scoreData] = await Promise.all([
    getRoomData(),
    getEntityData(),
    getScoreData(),
  ]);
  room.setData(
    Object.entries(roomData.entities).map(([id, entity]) => ({ id, ...entity }))
  );
  // Use timeout so the browser doesn't scroll to the new data when
  // this is triggered by the user directly
  setTimeout(() => {
    document.querySelector("#details-area").innerHTML = entityData
      ? JSON.stringify(entityData, null, 2)
      : "";
    document.querySelector("#steps").innerHTML = `Steps: ${roomData.steps}`;
    document.querySelector("#score").innerHTML = `Score: ${
      scoreData !== null ? scoreData : "-"
    }`;
  }, 0);
}

async function getRoomData() {
  const response = await fetch(`/api/rooms/${roomId}`);
  const data = await response.json();
  return data;
}

async function getEntityData() {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}`
    );
    if (!response.ok) {
      return null;
    }
    const entity = await response.json();
    return entity;
  } else {
    return null;
  }
}

async function getScoreData() {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}/score`
    );
    if (!response.ok) {
      return null;
    }
    const score = await response.json();
    return score;
  } else {
    return null;
  }
}

async function step() {
  await fetch(`/api/rooms/${roomId}/step`, { method: "POST" });
  update();
}

async function takeManualAction(action) {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}`
    );
    const { ai: oldAi, ...rest } = await response.json();
    await fetch(`/api/rooms/${roomId}/entities/${highlighted}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ai: { kind: "singular", move: action }, ...rest }),
    });
    await fetch(`/api/rooms/${roomId}/step`, { method: "POST" });
    const newResponse = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}`
    );
    const entity = await newResponse.json();
    await fetch(`/api/rooms/${roomId}/entities/${highlighted}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...entity, ai: oldAi }),
    });
    update();
  }
}

function toggleAutoStep() {
  if (autoStepTimer) {
    clearInterval(autoStepTimer);
    autoStepTimer = null;
  } else {
    autoStepTimer = setInterval(step, 400);
  }
}

async function evaluateChallenge(challenge, duration) {
  document.querySelector("#details-area").innerHTML = "...";
  const response = await fetch(`/api/evaluate`, {
    method: "POST",
    body: JSON.stringify({
      challenge,
      duration,
      profileTime: true,
      profileMemory: true,
    }),
  });
  const result = await response.json();
  document.querySelector("#details-area").innerHTML = JSON.stringify(
    result,
    null,
    2
  );
}

getChallenges();
initRoom(currentChallenge);
document
  .querySelector("#restart-button")
  .addEventListener("click", function () {
    initRoom(currentChallenge);
    this.blur();
  });
document
  .querySelector("#challenge-dropdown")
  .addEventListener("change", function (event) {
    const challenge = event.target.value;
    initRoom(challenge);
    this.blur();
  });
document
  .querySelector("#evaluate-button")
  .addEventListener("click", function (event) {
    const challenge = document.querySelector("#challenge-dropdown").value;
    const duration = document.querySelector("#duration-input").value;
    evaluateChallenge(challenge, duration);
    this.blur();
  });
document.addEventListener("keydown", (event) => {
  if (event.target !== document.body) {
    return;
  }
  event.preventDefault();
  switch (event.key) {
    case " ":
      step();
      break;
    case "ArrowLeft":
      takeManualAction("move_left");
      break;
    case "ArrowRight":
      takeManualAction("move_right");
      break;
    case "ArrowDown":
      takeManualAction("move_down");
      break;
    case "ArrowUp":
      takeManualAction("move_up");
      break;
    case "Control":
      takeManualAction("pick_up");
      break;
    case "a":
      toggleAutoStep();
      break;
    default:
      break;
  }
});
