// main.js
import './assets/main.css';

import App from './App.vue';
import { createApp } from "vue";
import PrimeVue from "primevue/config";
import Lara from "@/presets/lara"; // Import preset
import router from './router'; // Import the router

const app = createApp(App);
app.use(PrimeVue, {
  unstyled: true,
  pt: Lara, // Apply preset
});
app.use(router); // Add router to the app instance


app.mount("#app");
