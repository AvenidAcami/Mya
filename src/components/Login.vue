<template>
  <div id="mainLoginBlock">
    <h2>Вход</h2>
    <div id="loginPlaceholders">
      <input v-model="loginData.username" placeholder="Username" class="mainInfoPlaceholders"/>
      <input type="password" v-model="loginData.password" placeholder="Password" class="mainInfoPlaceholders" />
    </div>
    <button @click="login" class="loginButton">Login</button>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
  </div>
</template>
  
<script>
  
export default {
  data() {
    return {
      loginData: { username: '', password: '' },
      errorMessage: ''
    };
  },
  methods: {
    login() {
      this.$emit('login', this.loginData);
    }
  }
};
</script>


<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: url('../assets/wallpaper_1551_1920x1080.jpg') no-repeat center center fixed;
  background-size: cover;
}

#mainLoginBlock {
  background-color: rgba(255, 255, 255, 0.9); /* Полупрозрачный белый фон */
  border-radius: 10px;
  padding: 40px;
  width: 300px;
  margin: 100px auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  color: #3e4da2; /* Темно-синий цвет */
  margin-bottom: 20px;
}

.mainInfoPlaceholders {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #3e4da2; /* Темно-синий цвет */
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.mainInfoPlaceholders:focus {
  border-color: #5e71dc; /* Светло-синий цвет */
  outline: none;
}

.loginButton {
  background-color: #3e4da2; /* Темно-синий цвет */
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.loginButton:hover {
  background-color: #5e71dc; /* Светло-синий цвет */
}

.error-message {
  color: red;
  margin-top: 10px;
}

</style>