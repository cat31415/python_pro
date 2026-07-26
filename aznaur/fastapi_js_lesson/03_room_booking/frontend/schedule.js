const list = document.querySelector("#scheduleList");
const dateInput = document.querySelector("#scheduleDate");
const message = document.querySelector("#pageMessage");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers ?? {}) },
    ...options,
  });
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail ?? "Ошибка сервера");
  return data;
}

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = String(value);
  return element.innerHTML;
}

function localDateValue(date = new Date()) {
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
}

function hour(value) {
  return `${String(value).padStart(2, "0")}:00`;
}

async function loadSchedule() {
  list.innerHTML = '<p class="empty-state">Загружаем встречи…</p>';
  message.textContent = "";
  try {
    const data = await api(`/api/bookings?date=${encodeURIComponent(dateInput.value)}`);
    document.querySelector("#scheduleSummary").textContent = `${data.items.length} встреч на ${dateInput.value}`;
    list.innerHTML = data.items.length ? data.items.map((booking) => `
      <article class="booking-row">
        <span class="time">${hour(booking.start_hour)}</span>
        <div><h3>${escapeHtml(booking.room_name)}</h3><p>${booking.duration_hours} ч · до ${hour(booking.start_hour + booking.duration_hours)}</p></div>
        <span class="person">${escapeHtml(booking.employee)}</span>
        <button class="cancel-button" type="button" data-booking-id="${booking.id}">Отменить</button>
      </article>
    `).join("") : '<p class="empty-state">На эту дату встреч нет. Переговорные свободны.</p>';
  } catch (error) {
    list.innerHTML = `<p class="empty-state">API пока не отвечает: ${escapeHtml(error.message)}<br>Реализуйте GET /api/bookings?date=... в main.py.</p>`;
  }
}

list.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-booking-id]");
  if (!button) return;
  button.disabled = true;
  try {
    await api(`/api/bookings/${button.dataset.bookingId}`, { method: "DELETE" });
    await loadSchedule();
  } catch (error) {
    message.className = "message error";
    message.textContent = error.message;
    button.disabled = false;
  }
});

const params = new URLSearchParams(window.location.search);
dateInput.value = params.get("date") || localDateValue();
dateInput.addEventListener("change", () => {
  window.history.replaceState(null, "", `/schedule?date=${encodeURIComponent(dateInput.value)}`);
  loadSchedule();
});

loadSchedule();
