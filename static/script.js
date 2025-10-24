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
        div.innerHTML = `<span>${name}</span><span>${points} баллов</span>`;
        table.appendChild(div);
    });
}

async function addUser() {
    const name = prompt("Имя и фамилия:");
    if (!name) return;
    const points = parseInt(prompt("Количество баллов (можно отрицательное):") || "0");
    await fetch("/api/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, points})
    });
    await loadData();
}

async function changePoints() {
    const name = prompt("Кому изменить баллы?");
    if (!name) return;
    const points = parseInt(prompt("Изменение (например, 5 или -10):") || "0");
    await fetch("/api/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, points})
    });
    await loadData();
}

async function deleteUser() {
    const name = prompt("Кого удалить?");
    if (!name) return;
    if (!confirm(`Удалить ${name}?`)) return;
    await fetch("/api/delete", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });
    await loadData();
}

document.getElementById("search").addEventListener("input", (e) => {
    renderTable(e.target.value);
});

loadData();
