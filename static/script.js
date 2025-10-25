let data = {};

async function loadData() {
    const res = await fetch("/api/data");
    data = await res.json();
    renderTable();
}

function renderTable(filter = "") {
    const table = document.getElementById("table");
    table.innerHTML = "";
    const entries = Object.entries(data)
        .filter(([name]) => name.toLowerCase().includes(filter.toLowerCase()));
    entries.forEach(([name, points]) => {
        const div = document.createElement("div");
        div.className = "person";
        div.innerHTML = `<span class="name" onclick="editUser('${name}')">${name}</span><span>${points} баллов</span>`;
        table.appendChild(div);
    });
}

async function addUser() {
    const username = window.Telegram.WebApp.initDataUnsafe?.user?.username || '';
    if (!['Pavel_Skobyolkin', 'dariaskob', 'Wolfram183', 'artem_Christian'].includes(username)) {
        alert("У вас нет прав для редактирования!");
        return;
    }
    const name = prompt("Имя и фамилия:");
    if (!name) return;
    const points = parseInt(prompt("Количество баллов (можно отрицательное):") || "0");
    const response = await fetch("/api/add", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-Telegram-Username": username},
        body: JSON.stringify({name, points})
    });
    const result = await response.json();
    if (result.status === "error") alert(result.message);
    await loadData();
}

async function changePoints() {
    const username = window.Telegram.WebApp.initDataUnsafe?.user?.username || '';
    if (!['Pavel_Skobyolkin', 'dariaskob', 'Wolfram183', 'artem_Christian'].includes(username)) {
        alert("У вас нет прав для редактирования!");
        return;
    }
    const name = prompt("Кому изменить баллы?");
    if (!name) return;
    const points = parseInt(prompt("Изменение (например, 5 или -10):") || "0");
    const response = await fetch("/api/add", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-Telegram-Username": username},
        body: JSON.stringify({name, points})
    });
    const result = await response.json();
    if (result.status === "error") alert(result.message);
    await loadData();
}

async function deleteUser() {
    const username = window.Telegram.WebApp.initDataUnsafe?.user?.username || '';
    if (!['Pavel_Skobyolkin', 'dariaskob', 'Wolfram183', 'artem_Christian'].includes(username)) {
        alert("У вас нет прав для редактирования!");
        return;
    }
    const name = prompt("Кого удалить?");
    if (!name) return;
    if (!confirm(`Удалить ${name}?`)) return;
    const response = await fetch("/api/delete", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-Telegram-Username": username},
        body: JSON.stringify({name})
    });
    const result = await response.json();
    if (result.status === "error") alert(result.message);
    await loadData();
}

async function editUser(name) {
    const username = window.Telegram.WebApp.initDataUnsafe?.user?.username || '';
    if (!['Pavel_Skobyolkin', 'dariaskob', 'Wolfram183', 'artem_Christian'].includes(username)) {
        alert("У вас нет прав для редактирования!");
        return;
    }
    const newName = prompt("Новое ФИО (оставьте пустым для пропуска):", name);
    const pointsChange = prompt("Изменение баллов (например, 5 или -10, оставьте пустым для пропуска):", "");
    if (newName !== null || pointsChange !== null) {
        if (newName && newName !== name) {
            await fetch("/api/delete", {
                method: "POST",
                headers: {"Content-Type": "application/json", "X-Telegram-Username": username},
                body: JSON.stringify({name})
            });
            await fetch("/api/add", {
                method: "POST",
                headers: {"Content-Type": "application/json", "X-Telegram-Username": username},
                body: JSON.stringify({name: newName, points: pointsChange ? parseInt(pointsChange) : 0})
            });
        } else if (pointsChange !== null) {
            const points = parseInt(pointsChange) || 0;
            await fetch("/api/add", {
                method: "POST",
                headers: {"Content-Type": "application/json", "X-Telegram-Username": username},
                body: JSON.stringify({name, points})
            });
        }
        await loadData();
    }
}

document.getElementById("search").addEventListener("input", (e) => {
    renderTable(e.target.value);
});

loadData();
