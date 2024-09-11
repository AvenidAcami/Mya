// Загрузка кабинетов
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
        addComputerButton.textContent = 'Добавить оборудование';
        addComputerButton.onclick = () => showComputerForm(cabinet.name);

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn';
        deleteButton.textContent = 'x';
        deleteButton.onclick = () => deleteCabinet(cabinet.name);

        const computerList = document.createElement('div');
        computerList.id = `computers-${cabinet.name}`;
        computerList.className = 'computer-list';
        computerList.style.display = 'none'; // Изначально скрываем список оборудования

        buttonsDiv.appendChild(button);
        buttonsDiv.appendChild(addComputerButton);
        buttonsDiv.appendChild(deleteButton);
        cabinetDiv.appendChild(buttonsDiv);
        cabinetDiv.appendChild(computerList);

        cabinetList.appendChild(cabinetDiv);
    });
}

// Функция для открытия/закрытия списка оборудования
function toggleComputers(cabinetName) {
    const computerList = document.getElementById(`computers-${cabinetName}`);
    if (computerList.style.display === 'none') {
        computerList.style.display = 'block';
        loadComputers(cabinetName); // Загружаем список оборудования при первом открытии
    } else {
        computerList.style.display = 'none';
    }
}

// Добавление кабинета
function addCabinet() {
    const cabinetName = prompt("Введите название кабинета:");
    if (!cabinetName) return;

    fetch('/add_cabinet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: cabinetName })
    }).then(response => {
        if (response.status === 204) {
            loadCabinets();
        } else {
            alert("Кабинет с таким названием уже существует.");
        }
    });
}

// Добавление компьютера
function showComputerForm(cabinetName) {
    const contentDiv = document.querySelector('.content');
    contentDiv.innerHTML = `
        <h2>Добавить оборудование в кабинет ${cabinetName}</h2>
        <form id="add-computer-form">
            <label for="name">Название оборудования:</label>
            <input type="text" id="name" name="name" required><br>

            <label for="type">Тип оборудования:</label>
            <select id="type" name="type">
                <option value="comp">Компьютер</option>
                <option value="laptop">Ноутбук</option>
                <option value="monitor">Монитор</option>
                <option value="projector">Проектор</option>
                <option value="printer">Принтер</option>
                <option value="monoblock">Моноблок</option>
                <option value="interactive_board">Интерактивная доска</option>
            </select><br>

            <button type="submit">Добавить оборудование</button>
        </form>
    `;

    document.getElementById('add-computer-form').addEventListener('submit', async function (event) {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const type = document.getElementById('type').value;

        await fetch('/add_computer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cabinet_name: cabinetName, name, type })
        });

        loadComputers(cabinetName);
    });
}

// Загрузка оборудования в кабинете
async function loadComputers(cabinetName) {
    const response = await fetch(`/get_computers/${cabinetName}`);
    const computers = await response.json();
    const computerList = document.getElementById(`computers-${cabinetName}`);
    computerList.innerHTML = '';

    computers.forEach(computer => {
        const computerDiv = document.createElement('div');
        computerDiv.className = 'computer-item';
        computerDiv.setAttribute('data-name', computer.name); // Добавляем атрибут data-name

        const computerButton = document.createElement('button');
        computerButton.className = 'to_computer';
        computerButton.textContent = computer.name;
        computerButton.onclick = () => showCharacteristicsForm(cabinetName, computer.name);

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-computer-btn';
        deleteButton.textContent = 'x';
        deleteButton.onclick = () => deleteComputer(cabinetName, computer.name);

        computerDiv.appendChild(computerButton);
        computerDiv.appendChild(deleteButton);
        computerList.appendChild(computerDiv);
    });
}




// Показ формы для ввода характеристик с уже существующими значениями
async function showCharacteristicsForm(cabinetName, computerName) {
    const contentDiv = document.querySelector('.content');
    contentDiv.innerHTML = `<h2>Характеристики для ${computerName}</h2>
        <form id="characteristics-form">
            <div id="characteristics-container"></div>
            <button type="submit">Сохранить характеристики</button>
        </form>`;

    const response = await fetch(`/get_characteristics/${cabinetName}/${computerName}`);
    const characteristics = await response.json();

    const container = document.getElementById('characteristics-container');
    container.innerHTML = '';

    characteristics.forEach(characteristic => {
        const label = document.createElement('label');
        label.textContent = characteristic.name;

        const input = document.createElement('input');
        input.type = 'text';
        input.name = characteristic.name;
        input.value = characteristic.value;

        container.appendChild(label);
        container.appendChild(input);
        container.appendChild(document.createElement('br'));
    });

    const form = document.getElementById('characteristics-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        await fetch(`/save_characteristics/${cabinetName}/${computerName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ characteristics: data })
        });

        alert('Характеристики сохранены!');
    });
}

// Удалить кабинет
async function deleteCabinet(cabinetName) {
    if (!confirm(`Вы уверены, что хотите удалить кабинет "${cabinetName}"? Это действие удалит все оборудование и характеристики.`)) {
        return;
    }

    const response = await fetch(`/delete_cabinet/${cabinetName}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        alert(`Кабинет "${cabinetName}" был успешно удален.`);
        loadCabinets();  // Перезагрузка списка кабинетов
    } else {
        alert('Ошибка при удалении кабинета.');
    }
}

// Удаление оборудования
async function deleteComputer(cabinetName, computerName) {
    if (!confirm(`Вы уверены, что хотите удалить оборудование "${computerName}"? Все связанные характеристики будут удалены.`)) {
        return;
    }

    const response = await fetch(`/delete_computer/${cabinetName}/${computerName}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        alert(`Оборудование "${computerName}" было успешно удалено.`);

        // Находим и удаляем элемент оборудования из DOM через атрибут data-name
        const computerDiv = document.querySelector(`#computers-${cabinetName} .computer-item[data-name="${computerName}"]`);
        if (computerDiv) {
            computerDiv.remove();
        }
    } else {
        alert('Ошибка при удалении оборудования.');
    }
}




document.addEventListener('DOMContentLoaded', loadCabinets);
