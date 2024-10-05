<template>
    <div>
      <h2>Protected Page</h2>
      <p>This is a protected area. You can access this only when logged in.</p>
      <router-link to="/">Home</router-link>
      <button @click="fetchProtectedData">Fetch Protected Data</button>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
      data() {
          return {
              message: ''
          };
      },
      methods: {
          async fetchProtectedData() {
              try {
                  const token = localStorage.getItem('token');
                  const response = await axios.get('http://localhost:5000/protected', {
                      headers: { Authorization: `Bearer ${token}` }
                  });
                  this.message = response.data.msg;
              } catch (err) {
                  this.message = 'Error fetching protected data';
              }
          }
      }
  };
  </script>
  