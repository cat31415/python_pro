const grid = document.querySelector("#bookGrid");
const searchInput = document.querySelector("#search");
const genreSelect = document.querySelector("#genre");
let favoriteIds = new Set();

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

function bookCard(book) {
  const saved = favoriteIds.has(book.id);
  const genreClass = String(book.genre).toLowerCase().replace(/[^a-z]/g, "");
  return `
    <article class="book-card">
      <div class="book-cover ${genreClass}">
        <span class="cover-letter">${escapeHtml(book.title.charAt(0))}</span>
        <span class="cover-year">${book.year}</span>
      </div>
      <p class="book-meta">${escapeHtml(book.genre)}</p>
      <h3>${escapeHtml(book.title)}</h3>
      <p class="author">${escapeHtml(book.author)}</p>
      <p class="description">${escapeHtml(book.description)}</p>
      <button class="save-button ${saved ? "saved" : ""}" type="button" data-book-id="${book.id}" ${saved ? "disabled" : ""}>
        ${saved ? "Уже в избранном" : "Добавить в избранное"}
      </button>
    </article>
  `;
}

async function loadCatalog() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.set("query", searchInput.value.trim());
  if (genreSelect.value) params.set("genre", genreSelect.value);

  grid.innerHTML = '<p class="empty-state">Ищем книги…</p>';
  try {
    const data = await api(`/api/books?${params.toString()}`);
    document.querySelector("#resultsCount").textContent = `${data.total} книг`;
    grid.innerHTML = data.items.length
      ? data.items.map(bookCard).join("")
      : '<p class="empty-state">Ничего не найдено. Попробуйте другой запрос.</p>';
  } catch (error) {
    grid.innerHTML = `<p class="empty-state">API пока не отвечает: ${escapeHtml(error.message)}<br>Начните с GET /api/books в main.py.</p>`;
  }
}

async function loadInitialData() {
  try {
    const [genres, favorites] = await Promise.all([
      api("/api/genres"),
      api("/api/favorites"),
    ]);
    genreSelect.insertAdjacentHTML("beforeend", genres.items.map((genre) => `<option value="${escapeHtml(genre)}">${escapeHtml(genre)}</option>`).join(""));
    favoriteIds = new Set(favorites.items.map((book) => book.id));
    document.querySelector("#favoriteCount").textContent = favoriteIds.size;
  } catch (_error) {
    // Основная область покажет понятную ошибку контракта.
  }
  await loadCatalog();
}

grid.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-book-id]");
  if (!button) return;
  button.disabled = true;
  try {
    const book = await api("/api/favorites", {
      method: "POST",
      body: JSON.stringify({ book_id: Number(button.dataset.bookId) }),
    });
    favoriteIds.add(book.id);
    document.querySelector("#favoriteCount").textContent = favoriteIds.size;
    button.textContent = "Уже в избранном";
    button.classList.add("saved");
  } catch (error) {
    button.disabled = false;
    button.textContent = error.message;
  }
});

document.querySelector("#searchButton").addEventListener("click", loadCatalog);
genreSelect.addEventListener("change", loadCatalog);
searchInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadCatalog();
});

loadInitialData();
