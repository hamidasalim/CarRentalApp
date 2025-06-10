<!-- src/AppLayout.vue -->
<script setup>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import Home from '@/views/section/Home.vue';
import About from '@/views/section/About.vue';
import Services from '@/views/section/Services.vue';
import Contact from '@/views/section/Contact.vue';
</script>

<template>

  <main class="bg-gray-50">
    <!-- Each section on the same page with an ID for smooth scrolling -->
    <section id="home"><Home /></section>
    <section id="about"><About /></section>
    <section id="services"><Services /></section>
    <section id="contact"><Contact /></section>
  </main>

</template>

<style scoped>
section {
  padding: 4rem 0; /* Adds space around each section */
}
</style>
