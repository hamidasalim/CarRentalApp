<script setup>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { useRoute } from 'vue-router'; // Import useRoute to get the current route

const route = useRoute(); // Access the current route
</script>

<template>
  <header v-if="route.path !== '/login' && route.path !== '/register'">
    <Navbar />
  </header>
  
  <main :class="{ 'bg-gray-50': route.path !== '/login' && route.path !== '/register', 'full-page': route.path === '/login' || route.path === '/register' }">
    <router-view /> <!-- This renders the component based on the current route -->
  </main>
  
  <footer v-if="route.path !== '/login' && route.path !== '/register'">
    <Footer />
  </footer>
</template>

<style scoped>
/* Add full-page class to take the entire view for login/register */
.full-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa; /* Or any background color you prefer */
}
</style>
