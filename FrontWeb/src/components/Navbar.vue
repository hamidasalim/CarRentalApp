<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api'; // Adjust the path as needed

const menu = ref([
  { label: 'Home', route: '/#home' },
  { label: 'About', route: '/#about' },
  { label: 'Offers', route: '/#services' },
  { label: 'Contact', route: '/#contact' }
]);

const menuOpen = ref(false);
const showDropdown = ref(false); // Control dropdown visibility
const router = useRouter();
const profile = ref({}); // Holds user profile data

const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(''); // Message to display in the alert modal

const isLoggedIn = computed(() => !!localStorage.getItem('token')); // Check login status

const fetchProfile = async () => {
  try {
    const email = localStorage.getItem('email'); // Get email from localStorage
    if (!email) {
      console.error('No email found in local storage.');
      return;
    }

    const response = await api.post('/users/getUser', { email }); // Adjust the API endpoint if needed
    if (response?.data?.user) {
      profile.value = response.data.user; // Populate the profile data
    }
  } catch (error) {
    console.error('Failed to fetch profile:', error);
  }
};

// Fetch profile only if the user is logged in
onMounted(() => {
  if (isLoggedIn.value) {
    fetchProfile();
  }
});

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

const handleLogout = () => {
  // Remove token and email from localStorage
  localStorage.removeItem('token');
  localStorage.removeItem('email');

  // Redirect to login page
  setTimeout(() => {
    router.push('/login');
  }, 500); // Adjust the delay as needed
};

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};
</script>

<template>
  <nav class="border-gray-200 mx-4 fixed top-0 inset-x-0 z-[999]">
    <div
      class="lg:max-w-screen-xl bg-primary rounded-md md:rounded-full backdrop-blur-lg backdrop-grayscale mt-2 absolute inset-x-0 flex flex-wrap items-center justify-between mx-auto py-4 px-8 z-[9999]">
      <a aria-label="icon-rental" title="LOGO" href="#"
        class="text-2xl relative z-50 px-4 font-bold text-sky-950 font-poppins rounded-lg focus:outline-none focus:shadow-outline">
        Hamida's Rentals
      </a>
      <button aria-label="open menu" type="button" @click="toggleMenu"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm border-2 border-gray-200 text-gray-700 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200">
        <span class="sr-only">Open main menu</span>
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M1 1h15M1 7h15M1 13h15" />
        </svg>
      </button>
      <div :class="menuOpen ? 'block' : 'hidden'" class="w-full md:block md:w-auto" id="navbar-default">
        <ul
          class="font-medium flex flex-col items-center font-poppins p-4 text-base md:p-0 mt-4 border border-gray-100 rounded-lg md:flex-row md:space-x-8 md:mt-0 md:border-0 cursor-pointer">
          <li v-for="item in menu" :key="item.label">
            <router-link :to="item.route"
              class="block py-2 text-gray-700 rounded hover:opacity-45 ease-in-out duration-300">
              {{ item.label }}
            </router-link>
          </li>
          <li v-if="isLoggedIn">
            <router-link to="/contracts"
              class="block py-2 text-gray-700 rounded hover:opacity-45 ease-in-out duration-300">
              Contract List
            </router-link>
          </li>
          <li v-if="isLoggedIn">
            <router-link to="/payments"
              class="block py-2 text-gray-700 rounded hover:opacity-45 ease-in-out duration-300">
              Payment List
            </router-link>
          </li>
          <li v-if="isLoggedIn">
  <div class="relative dropdown" @click="toggleDropdown">
    <!-- Avatar Icon as Dropdown Trigger -->
    <div
      class="avatar-icon w-10 h-10 bg-cream rounded-full flex items-center justify-center cursor-pointer overflow-hidden">
      <template v-if="profile?.image_1920">
        <img :src="`data:image/png;base64,${profile.image_1920}`" alt="Profile Picture"
          class="w-full h-full object-cover" />
      </template>
      <template v-else>
        <svg class="w-6 h-6 text-gray-800" fill="currentColor" xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24">
          <path
            d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 4a3 3 0 11-.001 6.001A3 3 0 0112 6zm0 12c-2.67 0-5.34-1.17-7-3 .03-1.99 4-3.07 7-3.07 2.96 0 6.97 1.05 7 3.07-1.64 1.83-4.32 3-7 3z" />
        </svg>
      </template>
    </div>
    <!-- Dropdown Content -->
    <transition name="fade-slide">
      <div v-if="showDropdown"
        class="dropdown-content absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50">
        <router-link to="/profile"
          class="block px-4 py-2 text-gray-800 hover:bg-gray-100">Profile</router-link>
        <button @click="handleLogout"
          class="w-full text-left block px-4 py-2 text-gray-800 hover:bg-gray-100">Logout</button>
      </div>
    </transition>
  </div>
</li>


          <li v-else>
            <router-link to="/login"
              class="bg-cream hover:bg-creamhover py-2 px-4 rounded-full text-gray-800 font-semibold hover:scale-110 ease-in-out duration-500">
              Login
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.avatar-icon {
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.avatar-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}


.avatar-icon:hover {
  background-color: #d1d1d1;
}

.dropdown-content {
  position: absolute;
  right: 0;
  background-color: #fff;
  min-width: 160px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  z-index: 50;
  overflow: hidden;
  transform-origin: top right;
}

/* Dropdown content item */
.dropdown-content a,
.dropdown-content button {
  padding: 12px 20px;
  text-decoration: none;
  color: #333;
  display: block;
  width: 100%;
  transition: background-color 0.2s ease;
}

.dropdown-content a:hover,
.dropdown-content button:hover {
  background-color: #f1f1f1;
}

/* Dropdown Animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
