const taskList = document.querySelector("#taskList");
const form = document.querySelector("#taskForm");
const message = document.querySelector("#formMessage");
let tasks = [];
let currentFilter = "all";

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

function renderTasks() {
  const visibleTasks = tasks.filter((task) => {
    if (currentFilter === "active") return !task.done;
    if (currentFilter === "done") return task.done;
    return true;
  });

  const doneCount = tasks.filter((task) => task.done).length;
  const percent = tasks.length === 0 ? 0 : Math.round(doneCount / tasks.length * 100);
  document.querySelector("#progressText").textContent = `${doneCount} из ${tasks.length} завершено`;
  document.querySelector("#progressBar").style.width = `${percent}%`;

  if (visibleTasks.length === 0) {
    taskList.innerHTML = '<p class="empty-state">Здесь пока пусто. Добавьте задачу или смените фильтр.</p>';
    return;
  }

  const priorityNames = { low: "Низкий", medium: "Средний", high: "Высокий" };
  taskList.innerHTML = visibleTasks.map((task) => `
    <section class="task-card ${task.done ? "done" : ""}">
      <button class="toggle" type="button" data-toggle-id="${task.id}" aria-label="${task.done ? "Вернуть задачу в работу" : "Завершить задачу"}"></button>
      <div>
        <h3>${escapeHtml(task.title)}</h3>
        <span class="priority ${task.priority}">${priorityNames[task.priority] ?? escapeHtml(task.priority)}</span>
      </div>
      <button class="delete-button" type="button" data-delete-id="${task.id}" aria-label="Удалить задачу">×</button>
    </section>
  `).join("");
}

async function loadTasks() {
  try {
    const data = await api("/api/tasks");
    tasks = data.items;
    renderTasks();
  } catch (error) {
    taskList.innerHTML = `<p class="empty-state">API пока не отвечает: ${escapeHtml(error.message)}<br>Реализуйте GET /api/tasks в main.py.</p>`;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.className = "message";
  message.textContent = "Сохраняем…";

  const payload = {
    title: form.elements.title.value.trim(),
    priority: form.elements.priority.value,
  };

  try {
    const task = await api("/api/tasks", { method: "POST", body: JSON.stringify(payload) });
    tasks.push(task);
    form.reset();
    message.textContent = "Задача добавлена";
    renderTasks();
  } catch (error) {
    message.className = "message error";
    message.textContent = error.message;
  }
});

taskList.addEventListener("click", async (event) => {
  const toggle = event.target.closest("[data-toggle-id]");
  const deleteButton = event.target.closest("[data-delete-id]");

  try {
    if (toggle) {
      const task = tasks.find((item) => item.id === Number(toggle.dataset.toggleId));
      const updated = await api(`/api/tasks/${task.id}`, {
        method: "PATCH",
        body: JSON.stringify({ done: !task.done }),
      });
      tasks = tasks.map((item) => item.id === updated.id ? updated : item);
    }

    if (deleteButton) {
      const taskId = Number(deleteButton.dataset.deleteId);
      await api(`/api/tasks/${taskId}`, { method: "DELETE" });
      tasks = tasks.filter((item) => item.id !== taskId);
    }
    renderTasks();
  } catch (error) {
    message.className = "message error";
    message.textContent = error.message;
  }
});

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    currentFilter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.toggle("active", item === button));
    renderTasks();
  });
});

loadTasks();
