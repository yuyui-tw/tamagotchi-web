const message = document.querySelector("#message");
const conversation = document.querySelector("#conversation");
const form = document.querySelector("#command-form");
const commandInput = document.querySelector("#command");
const submitButton = form.querySelector("button");
const commands = new Map([
  ["餵食", "feed"],
  ["玩耍", "play"],
  ["睡覺", "sleep"],
  ["清潔", "clean"],
]);
const statNames = ["hunger", "mood", "energy", "cleanliness"];
const statusNames = {
  critical: "危急",
  hungry: "飢餓",
  sleepy: "睏倦",
  dirty: "髒亂",
  sad: "低落",
  happy: "愉快",
  normal: "正常",
};

function addLine(speaker, text) {
  const line = document.createElement("li");
  line.textContent = `${speaker}：${text}`;
  conversation.append(line);
}

function renderPet(pet) {
  for (const name of statNames) {
    document.querySelector(`#${name}`).textContent = `${pet[name]} / 100`;
  }
  document.querySelector("#status").textContent = statusNames[pet.status];
}

async function fetchPet(action) {
  const options = action
    ? {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      }
    : {};
  const response = await fetch(action ? "/api/pet/action" : "/api/pet", options);
  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.error || "無法更新寵物狀態。");
  }
  renderPet(result);
  message.textContent =
    result.message || `目前狀態：${statusNames[result.status]}`;
  return result;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const command = commandInput.value.trim();
  const action = commands.get(command);
  if (!action) {
    addLine("你", command);
    addLine("小雞", "我不懂這個操作，請輸入餵食、玩耍、睡覺或清潔。");
    commandInput.value = "";
    return;
  }

  addLine("你", command);
  submitButton.disabled = true;
  try {
    const result = await fetchPet(action);
    addLine("小雞", result.message);
  } catch (error) {
    addLine("小雞", error.message);
    message.textContent = error.message;
  } finally {
    commandInput.value = "";
    submitButton.disabled = commandInput.disabled;
    commandInput.focus();
  }
});

async function refreshPet() {
  try {
    await fetchPet();
  } catch (error) {
    message.textContent = error.message;
  }
}

fetchPet()
  .then((pet) => addLine("小雞", `目前狀態：${statusNames[pet.status]}`))
  .catch((error) => {
    message.textContent = error.message;
    addLine("小雞", error.message);
  });

window.setInterval(refreshPet, 1000);
