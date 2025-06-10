<template>
  <section
    class="login-container bg-gray-100 text-gray-800 font-poppins flex items-center justify-center min-h-screen px-4">
    <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
      <h2 class="text-3xl font-bold text-[#213363] mb-6 text-center">Login to Hamida's Rentals</h2>
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-lg font-semibold mb-2">Email</label>
          <input type="email" id="email" v-model="email" class="w-full p-3 border rounded-lg focus:outline-none"
            required />
        </div>

        <div>
          <label for="password" class="block text-lg font-semibold mb-2">Password</label>
          <input type="password" id="password" v-model="password"
            class="w-full p-3 border rounded-lg focus:outline-none" required />
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="text-red-500 text-sm text-center">{{ errorMessage }}</div>

        <!-- Submit Button -->
        <button type="submit"
          class="w-full bg-[#213363] text-white font-bold rounded-full py-3 hover:scale-105 transition-transform duration-300 ease-in-out">
          Login
        </button>
      </form>

      <!-- Register Link -->
      <p class="mt-4 text-center text-gray-700">
        Don’t have an account?
        <router-link to="/register" class="text-[#213363] font-semibold hover:underline">Register here</router-link>
      </p>

      <!-- Back to Home -->
      <button @click="goToHome"
        class="mt-6 w-full bg-gray-200 text-gray-800 font-semibold rounded-full py-3 hover:bg-gray-300 transition-transform duration-300 ease-in-out">
        Back to Home
      </button>
      <AlertModal :message="alertMessage" :visible="showAlert" @close="showAlert = false" />
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import AlertModal from "./AlertModal.vue"; // Adjust path as needed
const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(""); // Message to display in the alert modal

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const handleLogin = async () => {
  try {
    const requestData = {
      email: email.value,
      password: password.value,
    };

    const response = await api.post('/users/login', requestData);

    // Check if user data is in the response
    if (response.data.user) {
      // Store the token and transformed user details in localStorage
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('email', email.value);

      alertMessage.value = 'Login successful!';
      showAlert.value = true;
      setTimeout(() => {
        router.push('/'); // Redirect to home after the alert is shown
      }, 2000); // Adjust the delay (in milliseconds) as needed        } else {
    }
  } catch (error) {
    console.error('Error in handleLogin:', error.message);
    const message = error.response?.data?.error || 'Login failed. Please try again.';
    alertMessage.value = message; // Set the error message for the alert modal
    showAlert.value = true;
  }
};


const goToHome = () => {
  setTimeout(() => {
        router.push('/'); // Redirect to home after the alert is shown
      }, 500); // Adjust the delay (in milliseconds) as needed        } else {
};
</script>

<style scoped>
.login-container {
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

/* Media Queries */
@media (max-width: 768px) {
  .login-container {
    padding: 1rem 0.5rem;
  }

  .bg-white {
    padding: 1.5rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  button {
    font-size: 0.9rem;
  }
}

button {
  transition: transform 0.3s ease;
}
</style>
