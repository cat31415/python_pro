const grid = document.querySelector("#bookGrid");

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
      <button class="save-button remove-button" type="button" data-book-id="${book.id}">Убрать из избранного</button>
    </article>
  `;
}

async function loadFavorites() {
  try {
    const data = await api("/api/favorites");
    document.querySelector("#favoriteCount").textContent = data.items.length;
    document.querySelector("#resultsCount").textContent = `${data.items.length} книг`;
    grid.innerHTML = data.items.length
      ? data.items.map(bookCard).join("")
      : '<p class="empty-state">Полка пуста. Вернитесь в каталог и сохраните первую книгу.</p>';
  } catch (error) {
    grid.innerHTML = `<p class="empty-state">API пока не отвечает: ${escapeHtml(error.message)}<br>Реализуйте GET /api/favorites в main.py.</p>`;
  }
}

grid.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-book-id]");
  if (!button) return;
  button.disabled = true;
  try {
    await api(`/api/favorites/${button.dataset.bookId}`, { method: "DELETE" });
    await loadFavorites();
  } catch (error) {
    button.disabled = false;
    button.textContent = error.message;
  }
});

loadFavorites();
