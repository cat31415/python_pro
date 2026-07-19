const API = "";

const pageCopy = {
    booking: {
        title: "Сервис бронирования переговорок",
        subtitle: "Создание нового бронирования"
    },
    bookings: {
        title: "Бронирования",
        subtitle: "Список созданных бронирований"
    },
    rooms: {
        title: "Комнаты",
        subtitle: "Добавление новой переговорной"
    }
};

let rooms = [];

async function requestJSON(url, options) {
    const response = await fetch(`${API}${url}`, options);

    if (!response.ok) {
        let message = "Ошибка запроса";

        try {
            const error = await response.json();
            message = error.detail || message;
        } catch {
            message = await response.text() || message;
        }

        throw new Error(message);
    }

    return response.json();
}

function setEmptyRow(tableBody, text, columns) {
    tableBody.innerHTML = `
        <tr>
            <td class="empty-row" colspan="${columns}">${text}</td>
        </tr>
    `;
}

function formatDate(value) {
    if (!value) {
        return "";
    }

    return new Date(value).toLocaleString("ru-RU");
}

function getRoomName(roomId) {
    const room = rooms.find(item => item.id === roomId);

    if (!room) {
        return `#${roomId}`;
    }

    return `${room.name} (${room.size}${room.is_vip ? ", VIP" : ""})`;
}

async function loadRooms() {
    const select = document.getElementById("roomSelect");

    try {
        rooms = await requestJSON("/rooms");
    } catch (error) {
        rooms = [];
        console.error(error);
    }

    select.innerHTML = "";
    select.disabled = rooms.length === 0;

    if (rooms.length === 0) {
        const option = document.createElement("option");
        option.textContent = "Нет комнат";
        option.disabled = true;
        option.selected = true;
        select.appendChild(option);
    }

    rooms.forEach(room => {
        const option = document.createElement("option");
        option.value = room.id;
        option.textContent = `${room.name} (${room.size}${room.is_vip ? ", VIP" : ""})`;
        select.appendChild(option);
    });

    document.getElementById("roomsCount").textContent = rooms.length;
}

async function loadBookings() {
    const table = document.getElementById("bookingTable");

    try {
        const bookings = await requestJSON("/bookings");

        table.innerHTML = "";

        if (bookings.length === 0) {
            setEmptyRow(table, "Бронирований пока нет", 4);
        }

        bookings.forEach(booking => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${getRoomName(booking.room_id)}</td>
                <td>${booking.user_name}</td>
                <td>${formatDate(booking.start_time)}</td>
                <td>${formatDate(booking.end_time)}</td>
            `;

            table.appendChild(row);
        });

        document.getElementById("bookingsCount").textContent = bookings.length;
    } catch (error) {
        console.error(error);
        document.getElementById("bookingsCount").textContent = "0";
        setEmptyRow(table, "Не удалось загрузить бронирования", 4);
    }
}

function switchTab(tabName) {
    document.querySelectorAll(".nav-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.tab === tabName);
    });

    document.querySelectorAll(".tab-panel").forEach(panel => {
        panel.classList.remove("active");
    });

    document.getElementById(`${tabName}Panel`).classList.add("active");
    document.getElementById("pageTitle").textContent = pageCopy[tabName].title;
    document.getElementById("pageSubtitle").textContent = pageCopy[tabName].subtitle;

    if (tabName === "bookings") {
        loadBookings();
    }

    if (tabName === "booking") {
        loadRooms();
    }
}

document.querySelectorAll(".nav-tab").forEach(tab => {
    tab.addEventListener("click", () => switchTab(tab.dataset.tab));
});

document
    .getElementById("bookingForm")
    .addEventListener("submit", async event => {
        event.preventDefault();

        if (rooms.length === 0) {
            alert("Сначала добавьте комнату");
            switchTab("rooms");
            return;
        }

        const booking = {
            room_id: Number(document.getElementById("roomSelect").value),
            user_name: document.getElementById("employee").value.trim(),
            start_time: document.getElementById("start").value,
            end_time: document.getElementById("end").value
        };

        try {
            await requestJSON("/bookings", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(booking)
            });

            event.target.reset();
            alert("Бронирование создано");
            await loadBookings();
            switchTab("bookings");
        } catch (error) {
            alert(error.message);
        }
    });

document
    .getElementById("roomForm")
    .addEventListener("submit", async event => {
        event.preventDefault();

        const room = {
            id: Number(document.getElementById("roomId").value),
            name: document.getElementById("roomName").value.trim(),
            size: document.getElementById("roomSize").value,
            is_vip: document.getElementById("roomVip").checked
        };

        try {
            await requestJSON("/rooms", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(room)
            });

            event.target.reset();
            alert("Комната добавлена");
            await loadRooms();
            switchTab("booking");
        } catch (error) {
            alert(error.message);
        }
    });

async function init() {
    await loadRooms();
    await loadBookings();
}

init();
