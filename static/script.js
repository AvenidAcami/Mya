// Загрузка списка кабинетов
async function loadCabinets() {
    const response = await fetch('/get_cabinets');
    const cabinets = await response.json();
    const cabinetList = document.getElementById('cabinet-list');
    cabinetList.innerHTML = '';

    cabinets.forEach(cabinet => {
        const cabinetDiv = document.createElement('div');
        cabinetDiv.className = 'cabinet';

        const button = document.createElement('button');
        button.textContent = `Кабинет ${cabinet.name}`;
        button.onclick = () => toggleComputers(cabinet.id);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить кабинет';
        deleteButton.onclick = () => deleteCabinet(cabinet.id);

        const addComputerButton = document.createElement('button');
        addComputerButton.textContent = 'Добавить компьютер';
        addComputerButton.onclick = () => addComputer(cabinet.id);

        const computerList = document.createElement('div');
        computerList.id = `computers-${cabinet.id}`;
        computerList.className = 'computer-list';

        cabinetDiv.appendChild(button);
        cabinetDiv.appendChild(deleteButton);
        cabinetDiv.appendChild(addComputerButton);
        cabinetDiv.appendChild(computerList);

        cabinetList.appendChild(cabinetDiv);
    });
}

// Добавление нового кабинета
async function addCabinet() {
    const cabinetName = prompt('Введите номер кабинета:');
    if (cabinetName) {
        await fetch('/add_cabinet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: cabinetName })
        });
        loadCabinets();
    }
}

// Удаление кабинета
async function deleteCabinet(cabinetId) {
    if (confirm('Вы уверены, что хотите удалить этот кабинет?')) {
        await fetch(`/delete_cabinet/${cabinetId}`, { method: 'DELETE' });
        loadCabinets();
    }
}

// Переключение отображения списка компьютеров
async function toggleComputers(cabinetId) {
    const computerList = document.getElementById(`computers-${cabinetId}`);
    if (computerList.style.display === 'none' || computerList.style.display === '') {
        await loadComputers(cabinetId);
        computerList.style.display = 'block';
    } else {
        computerList.style.display = 'none';
    }
}

// Загрузка списка компьютеров в кабинете
async function loadComputers(cabinetId) {
    const response = await fetch(`/get_computers/${cabinetId}`);
    const computers = await response.json();
    const computerList = document.getElementById(`computers-${cabinetId}`);
    computerList.innerHTML = '';

    computers.forEach(computer => {
        const computerDiv = document.createElement('div');
        const computerLink = document.createElement('a');
        computerLink.href = `/computer/${cabinetId}/${computer.id}`;
        computerLink.textContent = `Компьютер: ${computer.name}`;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = () => deleteComputer(computer.id, cabinetId);

        computerDiv.appendChild(computerLink);
        computerDiv.appendChild(deleteButton);
        computerList.appendChild(computerDiv);
    });
}


// Добавление компьютера в кабинет
async function addComputer(cabinetId) {
    const computerName = prompt('Введите название компьютера:');
    if (computerName) {
        await fetch('/add_computer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cabinet_id: cabinetId, name: computerName })
        });
        await loadComputers(cabinetId);
    }
}

// Удаление компьютера
async function deleteComputer(computerId, cabinetId) {
    if (confirm('Вы уверены, что хотите удалить этот компьютер?')) {
        await fetch(`/delete_computer/${cabinetId}/${computerId}`, { method: 'DELETE' });
        await loadComputers(cabinetId);
    }
}


loadCabinets();
