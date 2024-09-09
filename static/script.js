// Загрузка списка кабинетов
async function loadCabinets() {
    try {
        const response = await fetch('/get_cabinets');
        const cabinets = await response.json();
        const cabinetList = document.getElementById('cabinet-list');
        cabinetList.innerHTML = '';

        cabinets.forEach(cabinet => {
            const cabinetDiv = document.createElement('div');
            cabinetDiv.className = 'cabinet';

            const button = document.createElement('button');
            button.textContent = `Кабинет ${cabinet.name}`;
            button.onclick = () => toggleComputers(cabinet.name); // Используем имя кабинета

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Удалить кабинет';
            deleteButton.onclick = () => deleteCabinet(cabinet.name); // Используем имя кабинета

            const addComputerButton = document.createElement('button');
            addComputerButton.textContent = 'Добавить компьютер';
            addComputerButton.onclick = () => addComputer(cabinet.name); // Используем имя кабинета

            const computerList = document.createElement('div');
            computerList.id = `computers-${cabinet.name}`; // Имя кабинета как идентификатор
            computerList.className = 'computer-list';

            cabinetDiv.appendChild(button);
            cabinetDiv.appendChild(deleteButton);
            cabinetDiv.appendChild(addComputerButton);
            cabinetDiv.appendChild(computerList);

            cabinetList.appendChild(cabinetDiv);
        });
    } catch (error) {
        console.error('Ошибка при загрузке кабинетов:', error);
    }
}

// Переключение отображения списка компьютеров
async function toggleComputers(cabinetName) {
    try {
        const computerList = document.getElementById(`computers-${cabinetName}`);
        if (computerList.style.display === 'none' || computerList.style.display === '') {
            await loadComputers(cabinetName); // Используем имя кабинета
            computerList.style.display = 'block';
        } else {
            computerList.style.display = 'none';
        }
    } catch (error) {
        console.error('Ошибка при переключении списка компьютеров:', error);
    }
}

// Загрузка компьютеров для кабинета
async function loadComputers(cabinetName) {
    try {
        const response = await fetch(`/get_computers/${encodeURIComponent(cabinetName)}`);
        const computers = await response.json();
        const computerList = document.getElementById(`computers-${cabinetName}`);
        computerList.innerHTML = '';

        computers.forEach(computer => {
            const computerDiv = document.createElement('div');

            // Ссылка на страницу компьютера
            const computerLink = document.createElement('a');
            computerLink.href = `/computer/${encodeURIComponent(cabinetName)}/${encodeURIComponent(computer.name)}`;
            computerLink.textContent = computer.name;

            // Кнопка для удаления компьютера
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Удалить компьютер';
            deleteButton.onclick = () => deleteComputer(computer.name, cabinetName);

            // Добавляем ссылку и кнопку удаления в элемент
            computerDiv.appendChild(computerLink);
            computerDiv.appendChild(deleteButton);

            computerList.appendChild(computerDiv);
        });
    } catch (error) {
        console.error('Ошибка при загрузке компьютеров:', error);
    }
}

// Добавление нового кабинета
async function addCabinet() {
    const cabinetName = prompt('Введите номер кабинета:');
    if (cabinetName) {
        try {
            await fetch('/add_cabinet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: cabinetName })
            });
            loadCabinets();
        } catch (error) {
            console.error('Ошибка при добавлении кабинета:', error);
        }
    }
}

// Добавление компьютера в кабинет
async function addComputer(cabinetName) {
    const computerName = prompt('Введите название компьютера:');
    if (computerName) {
        try {
            await fetch('/add_computer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cabinet_name: cabinetName, name: computerName }) // Передаем имя кабинета
            });
            await loadComputers(cabinetName); // Обновляем список компьютеров
        } catch (error) {
            console.error('Ошибка при добавлении компьютера:', error);
        }
    }
}

// Удаление кабинета
async function deleteCabinet(cabinetName) {
    if (confirm('Вы уверены, что хотите удалить этот кабинет?')) {
        try {
            await fetch(`/delete_cabinet/${encodeURIComponent(cabinetName)}`, { method: 'DELETE' });
            loadCabinets();
        } catch (error) {
            console.error('Ошибка при удалении кабинета:', error);
        }
    }
}

// Удаление компьютера
async function deleteComputer(computerName, cabinetName) {
    if (confirm('Вы уверены, что хотите удалить этот компьютер?')) {
        try {
            await fetch(`/delete_computer/${encodeURIComponent(cabinetName)}/${encodeURIComponent(computerName)}`, { method: 'DELETE' });
            await loadComputers(cabinetName);
        } catch (error) {
            console.error('Ошибка при удалении компьютера:', error);
        }
    }
}

// Инициализация списка кабинетов при загрузке страницы
loadCabinets();

// Добавляем кнопку для добавления нового кабинета
document.getElementById('add-cabinet-btn').addEventListener('click', addCabinet);
