<template>
    <div class="sidebar">
        <div v-for="eachCabinet in cabinetNamesList" :key="eachCabinet.id" class="eachCabinetButton">
            <button class="cabinetButton">{{ eachCabinet.name }}</button>
            <button class="addItemInCabinetButton">Добавить оборудование</button>
            <button class="deleteCabinetButton">x</button>
        </div>
        <div>
            <button id="addCabinetButton" @click="addCabinet">Добавить кабинет</button>
            <button id="toMainPage">На главную</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            cabinetNamesList: []
        };
    },
    methods: {
        async getCabinets() {
            this.cabinetNamesList = await fetchCabinets();
        },
        async addCabinet() {
            const cabinetName = prompt("Введите название кабинета:");
            if (!cabinetName) return;

            const response = await fetch('http://127.0.0.1:5001/add_cabinet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: cabinetName })
            });

            if (response.status === 204) {
                await this.getCabinets(); 
            } else {
                alert("Кабинет с таким названием уже существует.");
            }
        }
    },
    mounted() {
        this.getCabinets();
    }
};

async function fetchCabinets() {
    const response = await fetch('http://127.0.0.1:5001/getCabinets');
    const cabs = await response.json();
    return cabs;  
}
</script>


<style>
.sidebar {
    overflow: hidden;
    background-color: #5263c3;
    padding: 20px;
    width: 500px;
    color: white;
    border-right: 2px solid;
    border-color: #5555db;
    height: 79.5vh;
}
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
aside {
    display: block;
    unicode-bidi: isolate;
}

.eachCabinetButton{
    background-color: #3e4da2;
    margin-bottom: 10px;
    padding: 10px;
    display: block;
    justify-content: space-between;
    align-items: center;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    color: white;
}

.cabinetButton{
    background-color: #5e71dc;
    border: none;
    color: white;
    padding: 8px 12px;
    text-align: center;
    text-decoration: none;
    /* display: inline-block; */
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12pt;
    cursor: pointer;
    border-radius: 5px;
    margin-right: 6px;
    transition: background-color 0.3s ease;
    max-width: 100%;
    overflow: hidden;
    min-width: 150px;
    margin-top: 5px;
    margin-bottom: 5px;
}
.deleteCabinetButton {
    background-color: rgb(254, 102, 102);
    color: white;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    text-align: center;
    font-size: 14px;
    line-height: 24px;
    cursor: pointer;
    margin-left: 10px;
    margin-bottom: 5px;
}

.addItemInCabinetButton {
    background-color: #5e71dc;
    border: none;
    color: white;
    padding: 8px 12px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12pt;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s ease;
    width: 210px;
}

.addItemInCabinetButton:hover,
.cabinetButton:hover {
    background-color: #394462;
}

#addCabinetButton,
#toMainPage {
    background-color: #3e4da2;
    border: none;
    color: white;
    padding: 8px 12px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12pt;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 10px;
    transition: background-color 0.3s ease;
    margin-right: 5px;
}

#addCabinetButton:hover,
#toMainPage:hover {
    background-color: #394462;
}
</style>