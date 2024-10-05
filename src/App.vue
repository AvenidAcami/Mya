<template>
  <div id="app">
    <top-logo :logout="logout" v-if="isLoggedIn" />

    <div id="mainPageGuidePart" v-if="isLoggedIn">
      <mainaside></mainaside>
      <mainGuide></mainGuide>
    </div>

    

    <div v-if="!isLoggedIn">
      <Login @login="handleLogin" />
    </div>

    <div v-if="isLoggedIn">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import mainGuide from './components/mainGuide.vue';
import Login from './components/Login.vue';
import topLogo from './components/topLogo.vue';
import mainaside from './components/mainaside.vue';

export default {
  components: { Login, topLogo, mainaside, mainGuide},
  data() {
    return {
      isLoggedIn: false,
      role: null,
      token: null
    };
  },
  methods: {
    handleLogin(loginData) {
      axios.post('http://127.0.0.1:5001/login', loginData)
        .then(response => {
          this.token = response.data.access_token;
          this.isLoggedIn = true;
          const payload = JSON.parse(atob(this.token.split('.')[1]));
          this.role = payload.sub.role;
          localStorage.setItem('token', this.token);
        })
        .catch(() => {
          this.$refs.login.errorMessage = 'Login failed. Please check your credentials.';
        });
    },
    logout() {
      this.isLoggedIn = false;
      this.role = null;
      this.token = null;
      localStorage.removeItem('token');
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      this.token = token;
      this.isLoggedIn = true;
      const payload = JSON.parse(atob(this.token.split('.')[1]));
      this.role = payload.sub.role;
    }
  }
};
</script>

<style>
#mainPageGuidePart{
  display: flex;
}
</style>
