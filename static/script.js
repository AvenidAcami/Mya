// Загрузка списка кабинетов
async function loadCabinets() {
    const response = await fetch('/get_cabinets');
    const cabinets = await response.json();
    const cabinetList = document.getElementById('cabinet-list');
    cabinetList.innerHTML = '';

    cabinets.forEach(cabinet => {
        const cabinetDiv = document.createElement('div');
        cabinetDiv.className = 'cabinet';

        const buttonsDiv = document.createElement('div');
        buttonsDiv.className = 'cab_and_but_div';

        const button = document.createElement('button');
        button.className = 'cabinet_button';
        button.textContent = `Кабинет ${cabinet.name}`;
        button.onclick = () => toggleComputers(cabinet.name);

        const addComputerButton = document.createElement('button');
        addComputerButton.className = 'add-computer-btn';
        addComputerButton.textContent = 'Добавить компьютер';
        addComputerButton.onclick = () => addComputer(cabinet.name);

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn';
        deleteButton.textContent = '×';
        deleteButton.onclick = () => deleteCabinet(cabinet.name);

        const computerList = document.createElement('div');
        computerList.id = `computers-${cabinet.name}`;
        computerList.className = 'computer-list';

        buttonsDiv.appendChild(button);
        buttonsDiv.appendChild(addComputerButton);
        buttonsDiv.appendChild(deleteButton); 
        cabinetDiv.appendChild(buttonsDiv);  
        cabinetDiv.appendChild(computerList);

        cabinetList.appendChild(cabinetDiv);
    });
}

// Добавление компьютера в кабинет
async function addComputer(cabinetName) {
    const computerName = prompt('Введите название компьютера:');
    if (computerName) {
        await fetch('/add_computer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cabinet_name: cabinetName, name: computerName })
        });
        await loadComputers(cabinetName);
    }
}

// Переключение отображения списка компьютеров
async function toggleComputers(cabinetName) {
    const computerList = document.getElementById(`computers-${cabinetName}`);
    if (computerList.style.display === 'none' || computerList.style.display === '') {
        await loadComputers(cabinetName);
        computerList.style.display = 'block';
    } else {
        computerList.style.display = 'none';
    }
}

// Загрузка списка компьютеров в кабинете и отображение их как кнопок
async function loadComputers(cabinetName) {
    const response = await fetch(`/get_computers/${cabinetName}`);
    const computers = await response.json();
    const computerList = document.getElementById(`computers-${cabinetName}`);
    computerList.innerHTML = '';

    computers.forEach(computer => {
        const computerDiv = document.createElement('div');
        computerDiv.className = 'buttons_computer';

        // Теперь создаем кнопку вместо ссылки
        const computerButton = document.createElement('button');
        computerButton.className = 'to_computer';
        computerButton.textContent = computer.name;
        computerButton.onclick = () => loadComputerDetails(cabinetName, computer.name);  // При клике грузим информацию о компьютере

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn';
        deleteButton.textContent = '×';
        deleteButton.onclick = () => deleteComputer(computer.name, cabinetName);

        computerDiv.appendChild(computerButton);
        computerDiv.appendChild(deleteButton);
        computerList.appendChild(computerDiv);
    });
}

// Функция для загрузки данных компьютера и отображения в блоке .content
async function loadComputerDetails(cabinetName, computerName) {
    const response = await fetch(`/computer/${cabinetName}/${computerName}`);
    
    // Проверяем, был ли успешный ответ
    if (response.ok) {
        const htmlContent = await response.text(); // Получаем HTML от сервера

        // Обновляем содержимое блока content
        const contentDiv = document.querySelector('.content');
        contentDiv.innerHTML = htmlContent;
    } else {
        alert('Ошибка загрузки информации о компьютере.');
    }
}

// Удаление компьютера
async function deleteComputer(computerName, cabinetName) {
    if (confirm('Вы уверены, что хотите удалить этот компьютер?')) {
        await fetch(`/delete_computer/${cabinetName}/${computerName}`, { method: 'DELETE' });
        await loadComputers(cabinetName);
    }
}

// Удаление кабинета
async function deleteCabinet(cabinetName) {
    if (confirm('Вы уверены, что хотите удалить этот кабинет?')) {
        await fetch(`/delete_cabinet/${cabinetName}`, { method: 'DELETE' });
        loadCabinets();
    }
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

loadCabinets();
