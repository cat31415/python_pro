const roomList = document.querySelector("#roomList");
const form = document.querySelector("#bookingForm");
const message = document.querySelector("#formMessage");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers ?? {}) },
    ...options,
  });
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail[0]?.msg : data.detail;
    throw new Error(detail ?? "Ошибка сервера");
  }
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

async function loadRooms() {
  try {
    const data = await api("/api/rooms");
    roomList.innerHTML = data.items.map((room, index) => `
      <div class="room-option">
        <input type="radio" name="room" id="room-${room.id}" value="${room.id}" ${index === 0 ? "checked" : ""}>
        <label for="room-${room.id}">
          <span class="room-capacity">до ${room.capacity} человек</span>
          <h3>${escapeHtml(room.name)}</h3>
          <p class="equipment">${room.equipment.map(escapeHtml).join(" · ")}</p>
        </label>
      </div>
    `).join("");
  } catch (error) {
    roomList.innerHTML = `<p class="empty-state">API пока не отвечает: ${escapeHtml(error.message)}<br>Реализуйте GET /api/rooms в main.py.</p>`;
  }
}

const dateInput = document.querySelector("#date");
dateInput.min = localDateValue();
dateInput.value = localDateValue();

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.className = "message";
  message.textContent = "Проверяем расписание…";

  const selectedRoom = form.elements.room;
  if (!selectedRoom?.value) {
    message.className = "message error";
    message.textContent = "Сначала выберите комнату";
    return;
  }

  const payload = {
    room_id: Number(selectedRoom.value),
    employee: form.elements.employee.value.trim(),
    date: form.elements.date.value,
    start_hour: Number(form.elements.start_hour.value),
    duration_hours: Number(form.elements.duration_hours.value),
  };

  try {
    await api("/api/bookings", { method: "POST", body: JSON.stringify(payload) });
    message.textContent = "Комната забронирована. Открываем расписание…";
    window.setTimeout(() => {
      window.location.href = `/schedule?date=${encodeURIComponent(payload.date)}`;
    }, 500);
  } catch (error) {
    message.className = "message error";
    message.textContent = error.message;
  }
});

loadRooms();
