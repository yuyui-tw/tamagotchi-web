const message = document.querySelector("#message");
const statNames = ["hunger", "mood", "energy", "cleanliness"];

function renderPet(pet) {
  for (const name of statNames) {
    document.querySelector(`#${name}`).textContent = pet[name];
  }
}

async function requestPet(action) {
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
  message.textContent = "寵物狀態已更新。";
}

document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", async () => {
    try {
      await requestPet(button.dataset.action);
    } catch (error) {
      message.textContent = error.message;
    }
  });
});

requestPet().catch((error) => {
  message.textContent = error.message;
});
