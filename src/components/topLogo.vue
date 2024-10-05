<template>
    <div class="mainHeader">
      <img src="../assets/ugtu.jpeg" alt="Logo">
      <button @click="logout" id="logoutButton">Logout</button>
    </div>
</template>
  
<script>
  export default {
    props: {
      logout: {
        type: Function,
        required: true
      }
    }
  };
</script>
  
<style>
.mainHeader {
    background-color: #3e4da2;
    padding: 0;
    text-align: left;
    border-bottom: 2px solid;
    border-color: #383896;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-right: 10px;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
header {
  display: block;
  unicode-bidi: isolate;
}
body {
  font-family: Arial, sans-serif;
  background-color: #f0f8ff;
  color: #333;
}
#logoutButton{
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
    margin-top: 5px;
    margin-right: 6px;
    transition: background-color 0.3s ease;
    max-width: 100%;
    overflow: hidden;
    min-width: 150px;
}

#logoutButton:hover {
    background-color: #394462;
}

</style>
  