<script setup>
import { createHydrationRenderer } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="font-family: 'Press Start 2p'; font-size: 14">
      <a class="navbar-brand" href="/" style="margin-left:1%">
        <img class="img" src="/src/assets/logo.png" alt="logo quizz"/>
      </a>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li :class="[isAdmin ? 'hide' : 'nav-item active']">
            <router-link  class="nav-link" to="/admin">Admin</router-link>
          </li> 
          <li :class="[isAdmin ? 'nav-item active' : 'hide']">
            <router-link  class="nav-link" to="/">Log out</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </header>
  <div class="d-flex align-items-center justify-content-center mt-10">
    <RouterView/>
  </div>
</template>

<script>
  export default {
    name: "App",  
    computed: {
      isAdmin() {
        if (this.$router.currentRoute.value.path == '/admin-panel'   || 
            this.$router.currentRoute.value.path ==  '/new-question' || 
            this.$router.currentRoute.value.path ==  '/detail-question' || 
            this.$router.currentRoute.value.path ==  '/edit-question') {
              return true;
            }
        return false;   
      }
    }
    
  }
</script>

<style scoped>
  .mt-10 {
    margin-top: 10% !important
  }

  .hide {
    display: none;
  }
</style>
