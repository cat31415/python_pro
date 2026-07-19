const drinkList = document.querySelector("#drinkList");
const orderList = document.querySelector("#orderList");
const form = document.querySelector("#orderForm");
const message = document.querySelector("#formMessage");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers ?? {}) },
    ...options,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail ?? "Сервер не смог выполнить запрос");
  }
  return data;
}

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = String(value);
  return element.innerHTML;
}

async function loadDrinks() {
  try {
    const data = await api("/api/drinks");
    drinkList.innerHTML = data.items.map((drink, index) => `
      <div class="drink-option">
        <input type="radio" name="drink" id="drink-${drink.id}" value="${drink.id}" ${index === 0 ? "checked" : ""}>
        <label for="drink-${drink.id}">
          <span>${escapeHtml(drink.name)}<small>≈ ${drink.ready_minutes} мин</small></span>
          <strong>${drink.price} ₽</strong>
        </label>
      </div>
    `).join("");
  } catch (error) {
    drinkList.innerHTML = `<p class="form-message error">${escapeHtml(error.message)}</p>`;
  }
}

async function loadOrders() {
  try {
    const data = await api("/api/orders");
    const waiting = data.items.filter((order) => order.status === "waiting").length;
    document.querySelector("#waitingCount").textContent = waiting;
    document.querySelector("#readyCount").textContent = data.items.length - waiting;

    if (data.items.length === 0) {
      orderList.innerHTML = '<p class="muted">Очередь пуста. Можно заказывать первым.</p>';
      return;
    }

    orderList.innerHTML = data.items.map((order) => `
      <section class="order-card">
        <span class="order-number">#${order.id}</span>
        <div>
          <h3>${escapeHtml(order.customer)}</h3>
          <p>${escapeHtml(order.drink_name)} · ${order.price} ₽</p>
        </div>
        ${order.status === "ready"
          ? '<span class="ready-label">Готов</span>'
          : `<button class="status-button" type="button" data-ready-id="${order.id}">Заказ готов</button>`}
      </section>
    `).join("");
  } catch (error) {
    orderList.innerHTML = `<p class="form-message error">${escapeHtml(error.message)}</p>`;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.className = "form-message";
  message.textContent = "Отправляем заказ…";

  const selectedDrink = form.elements.drink;
  const payload = {
    customer: form.elements.customer.value.trim(),
    drink_id: Number(selectedDrink.value),
  };

  try {
    await api("/api/orders", { method: "POST", body: JSON.stringify(payload) });
    form.elements.customer.value = "";
    message.textContent = "Заказ добавлен в очередь";
    await loadOrders();
  } catch (error) {
    message.className = "form-message error";
    message.textContent = error.message;
  }
});

orderList.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-ready-id]");
  if (!button) return;

  button.disabled = true;
  try {
    await api(`/api/orders/${button.dataset.readyId}/ready`, { method: "PATCH" });
    await loadOrders();
  } catch (error) {
    message.className = "form-message error";
    message.textContent = error.message;
    button.disabled = false;
  }
});

document.querySelector("#refreshButton").addEventListener("click", loadOrders);

loadDrinks();
loadOrders();
