<template>
  <section
    class="register-container bg-gray-100 text-gray-800 font-poppins flex items-center justify-center min-h-screen">
    <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-4xl register-modal">
      <h2 class="text-3xl font-bold text-[#213363] mb-6 text-center">Create Your Account</h2>
      <form @submit.prevent="handleRegister" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left Column -->
        <div>
          <!-- Name -->
          <div>
            <label for="name" class="block text-lg font-semibold mb-2">Name</label>
            <input type="text" id="name" v-model="name" placeholder="Enter your name"
              class="w-full p-3 border rounded-lg focus:outline-none" required />
          </div>

          <!-- Email -->
          <div class="mt-4">
            <label for="email" class="block text-lg font-semibold mb-2">Email</label>
            <input type="email" id="email" v-model="email" placeholder="Enter your email"
              class="w-full p-3 border rounded-lg focus:outline-none" required />
          </div>

          <!-- Password -->
          <div class="mt-4">
            <label for="password" class="block text-lg font-semibold mb-2">Password</label>
            <input type="password" id="password" v-model="password" placeholder="At least 8 characters"
              class="w-full p-3 border rounded-lg focus:outline-none" minlength="8" maxlength="16" required />
          </div>

          <!-- Confirm Password -->
          <div class="mt-4">
            <label for="confirmPassword" class="block text-lg font-semibold mb-2">Confirm Password</label>
            <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Re-enter your password"
              class="w-full p-3 border rounded-lg focus:outline-none" required />
          </div>

          <!-- Address -->
          <div class="mt-4">
            <label class="block text-lg font-semibold mb-2">Address</label>
            <div class="grid grid-cols-2 gap-4">
              <input type="text" v-model="street" id="street" placeholder="Street"
                class="w-full p-3 border rounded-lg focus:outline-none" />
              <input type="text" v-model="street2" id="street2" placeholder="Street 2"
                class="w-full p-3 border rounded-lg focus:outline-none" />
              <input type="text" v-model="city" id="city" placeholder="City"
                class="w-full p-3 border rounded-lg focus:outline-none" />
              <input type="text" v-model="postalCode" id="postalCode" placeholder="Postal Code"
                class="w-full p-3 border rounded-lg focus:outline-none" />
            </div>
          </div>
        </div>

        <!-- Right Column -->
        <div>
          <!-- Mobile Number -->
          <div>
            <label for="mobile" class="block text-lg font-semibold mb-2">Mobile Number</label>
            <input type="text" id="mobile" v-model="mobile" placeholder="Enter your mobile number"
              class="w-full p-3 border rounded-lg focus:outline-none" required />
          </div>

          <!-- Date of Birth -->
          <div class="mt-4">
            <label for="dob" class="block text-lg font-semibold mb-2">Date of Birth</label>
            <input type="date" id="dob" v-model="dob" class="w-full p-3 border rounded-lg focus:outline-none"
              required />
          </div>

          <!-- CIN Details -->
          <div class="mt-4">
            <label for="cinNumber" class="block text-lg font-semibold mb-2">CIN Number</label>
            <input type="text" id="cinNumber" v-model="cinNumber" placeholder="Enter your CIN number"
              class="w-full p-3 border rounded-lg focus:outline-none" required />
          </div>
          <div class="mt-4">
            <label for="cinDate" class="block text-lg font-semibold mb-2">CIN Issue Date</label>
            <input type="date" id="cinDate" v-model="cinDate" class="w-full p-3 border rounded-lg focus:outline-none"
              required />
          </div>

          <!-- Driver's License Details -->
          <div class="mt-4">
            <label for="driverLicenseNumber" class="block text-lg font-semibold mb-2">Driver's License Number</label>
            <input type="text" id="driverLicenseNumber" v-model="driverLicenseNumber"
              placeholder="Enter your driver's license number" class="w-full p-3 border rounded-lg focus:outline-none"
              required />
          </div>
          <div class="mt-4">
            <label for="driverLicenseDate" class="block text-lg font-semibold mb-2">License Issue Date</label>
            <input type="date" id="driverLicenseDate" v-model="driverLicenseDate"
              class="w-full p-3 border rounded-lg focus:outline-none" required />
          </div>
          <div class="mt-4">
            <label for="driverLicenseCategory" class="block text-lg font-semibold mb-2">Driver's License
              Category</label>
            <input type="text" id="driverLicenseCategory" v-model="driverLicenseCategory"
              placeholder="Enter your driver's license Category" class="w-full p-3 border rounded-lg focus:outline-none"
              required />
          </div>
        </div>



        <!-- Submit Button (Full Width) -->
        <div class="col-span-1 md:col-span-2">
          <button type="submit"
            class="w-full bg-[#213363] text-white font-bold rounded-full py-3 hover:scale-105 transition-transform duration-300 ease-in-out">
            Register
          </button>
        </div>
      </form>
      <p class="mt-4 text-center text-gray-700">
        Already have an account?
        <router-link to="/login" class="text-[#213363] font-semibold hover:underline">Login here</router-link>
      </p>

      <button @click="goToHome"
        class="mt-6 w-full bg-gray-200 text-gray-800 font-semibold rounded-full py-3 hover:bg-gray-300 transition-transform duration-300 ease-in-out">
        Back to Home
      </button>
      <AlertModal
      :message="alertMessage"
      :visible="showAlert"
      @close="showAlert = false"
    />
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


const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const street = ref('');
const street2 = ref('');
const city = ref('');
const postalCode = ref('');
const mobile = ref('');
const dob = ref('');
const cinNumber = ref('');
const cinDate = ref('');
const driverLicenseNumber = ref('');
const driverLicenseCategory = ref('');
const driverLicenseDate = ref('');


const router = useRouter();



const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alertMessage.value = "Passwords do not match";
    showAlert.value = true;
    return;
  }


  try {


    const requestData = {
      name: name.value,
      email: email.value,
      password: password.value,
      street: street.value,
      street2: street2.value,
      city: city.value,
      postalCode: postalCode.value,
      mobile: mobile.value,
      dob: dob.value,
      cinNumber: cinNumber.value,
      cinDate: cinDate.value,
      driverLicenseNumber: driverLicenseNumber.value,
      driverLicenseCategory: driverLicenseCategory.value,
      driverLicenseDate: driverLicenseDate.value,

    };

    const response = await api.post('/users/register', requestData);
    if (response.data.result.message == "User registered successfully!"){
      alertMessage.value = "User registered successfully!";
    showAlert.value = true;
    setTimeout(() => {
        router.push('/login'); // Redirect to home after the alert is shown
      }, 2000); // Adjust the delay (in milliseconds) as needed        } else {

    }
    
     

    
  } catch (error) {
    const message = error.response?.data?.error || "Registration failed. Please try again.";
    alertMessage.value = message;
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
.register-container {
  background-color: #f8f9fa;
  margin-top: 350px;

}

.register-modal {
  margin-top: 180px;

}

button {
  transition: transform 0.3s ease;
}
</style>
