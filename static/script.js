// script.js
async function loadData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    displayData(data);
}

async function addUser() {
    const name = document.getElementById('name').value;
    const points = parseInt(document.getElementById('points').value) || 0;
    const response = await fetch('/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, points })
    });
    const result = await response.json();
    displayData(result.data);
}

async function deleteUser() {
    const name = document.getElementById('name').value;
    const response = await fetch('/api/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    const result = await response.json();
    displayData(result.data);
}

function displayData(data) {
    const dataDiv = document.getElementById('data');
    dataDiv.innerHTML = Object.entries(data).map(([name, points]) => `${name}: ${points}`).join('<br>');
}

// Проверка прав
async function checkPermissions() {
    const username = window.Telegram.WebApp.initDataUnsafe?.user?.username || '';
    const isEditor = ['Pavel_Skobyolkin'].includes(username); // Список редакторов
    document.getElementById('addForm').style.display = isEditor ? 'block' : 'none';
    document.getElementById('deleteForm').style.display = isEditor ? 'block' : 'none';
}

window.onload = () => {
    loadData();
    checkPermissions();
};
