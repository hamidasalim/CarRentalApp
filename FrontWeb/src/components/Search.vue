<template>
  <div class="search-results">
    <h1 class="results-title">Available Cars</h1>
    <p v-if="startDate && endDate" class="date-range">
      Showing cars available from <strong>{{ startDate }}</strong> to
      <strong>{{ endDate }}</strong>.
    </p>
    <p v-if="loading" class="loading-text">Loading available cars...</p>
    <p v-if="error" class="error-text">{{ error }}</p>



    <!-- Search Bar and Filter -->
    <div class="search-controls">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search..."
        class="search-bar"
      />
      <select v-model="searchType" class="search-type">
        <option value="">Search by</option>
        <option value="price">Price</option>
        <option value="model">Model</option>
      </select>
    </div>
<div v-if="!loading && !error && filteredCars.length" class="car-list">
  
  <div v-for="car in filteredCars" :key="car.id" class="car-card" @click="openBookingModal(car)">
    <img :src="car.image" :alt="car.name" class="car-image" />
    <div class="car-info">
      
      <p class="car-license"><strong>License Plate:</strong> {{ car.license_plate }}</p>
      <p class="car-model"><strong>Model:</strong> {{ extractCarName(car.name) }}</p>
      <p class="car-tarif"><strong>Tarif:</strong> {{ car.tarif }} TND per day</p>
    </div>
  </div>
</div>

    <p v-if="!loading && !error && !cars.length" class="no-results">
      No cars available for the selected dates. Please adjust your search.
    </p>

    <!-- Booking Modal -->
    <div v-if="showBookingModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-left">
          <img :src="selectedCar.image" alt="Car Image" class="car-image-large" />
          <div class="car-details">
            <p><strong>License Plate:</strong> {{ selectedCar.license_plate || 'N/A' }}</p>
            <p><strong>Model:</strong> {{ selectedCar.model || 'N/A' }}</p>
            <p><strong>Tarif:</strong> {{ selectedCar.tarif }} TND per day</p>
            <p><strong>Fuel Price:</strong> {{ fuelPrice }} TND</p>
            <p><strong>Total Price (No Tax):</strong> {{ totalPrice }} TND</p>

          </div>
          <div class="modal-actions">
            <button type="button" @click="handlePaymentPlus" class="cash-button">Pay in Cash</button>
          </div>
        </div>
        <div class="modal-right">
          <h2 class="modal-title">Book {{ selectedCar.name }}</h2>
          <form class="payment-form" @submit.prevent="handlePayment">
            <div class="payment-logos">
              <img src="/assets/visalogo.png" alt="Visa Logo" />
              <img src="/assets/mastercardlogo.png" alt="Mastercard Logo" />
            </div>
            <div class="form-group">
              <label for="cardNumber">Card Number</label>
              <input id="cardNumber" v-model="payment.cardNumber" placeholder="1234 5678 9012 3456" maxlength="19"
                required />
            </div>
            <div class="form-group form-inline">
              <div>
                <label for="expiryDate">Expiry Date</label>
                <input id="expiryDate" v-model="payment.expiryDate" placeholder="MM/YY" maxlength="5" required />
              </div>
              <div>
                <label for="cvv">CVV</label>
                <input id="cvv" v-model="payment.cvv" placeholder="123" maxlength="3" required />
              </div>
            </div>
            <div class="form-group">
              <label for="fuelLevel">Fuel Level</label>
              <select id="fuelLevel" v-model="payment.fuelLevel" class="fuel-level-dropdown" required>
                <option value="" default>Select Fuel Level</option>
                <option value="1/4">1/4</option>
                <option value="1/2">1/2</option>
                <option value="3/4">3/4</option>
                <option value="Plein">Plein</option>
              </select>
            </div>
            <div class="modal-actions">
              <button @click="handlePaymentOnline" class="confirm-button">Confirm Payment</button>
              <button type="button" @click="closeBookingModal" class="cancel-button">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <AlertModal
      :message="alertMessage"
      :visible="showAlert"
      :duration ="alertDuration"
      @close="showAlert = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch,computed } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';

import api from '@/api';
import axios from 'axios';
import AlertModal from "./AlertModal.vue"; // Adjust path as needed
const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(""); // Message to display in the alert modal
const alertDuration = ref("");
const searchQuery = ref(''); // Input for search text
const searchType = ref(''); // Dropdown for search type



const route = useRoute();
const startDate = ref('');
const endDate = ref('');
const cars = ref([]);
const loading = ref(true);
const error = ref(null);
const fuelPrice = ref('');
const totalPrice = ref('');
const router = useRouter();


onMounted(async () => {
  startDate.value = route.query.startDate || '';
  endDate.value = route.query.endDate || '';
  loading.value = true;

  try {
    const response = await api.post('/vehicles/available', {
      start_date: startDate.value,
      end_date: endDate.value,
    });

    if (response.data.result) {
      cars.value = response.data.result.available_cars.map((car) => ({
        ...car,
        image: car.picture ? `data:image/png;base64,${car.picture}` : '/assets/default-car.png',
      }));
    } else {
      cars.value = [];
    }
    loading.value = false;
  } catch (err) {
    error.value = 'Failed to fetch available cars. Please try again later.';
    console.error(err);
    loading.value = false;
  }
});
const extractCarName = (fullName) => {
  const parts = fullName.split('/');
  return parts.length >= 2 ? `${parts[0]}/${parts[1]}` : fullName;
};


const showBookingModal = ref(false);
const selectedCar = ref({});
const payment = ref({
  cardName: '',
  cardNumber: '',
  expiryDate: '',
  cvv: '',
});
const calculatePrices = () => {
  const days = Math.max(
    (new Date(endDate.value) - new Date(startDate.value)) / (1000 * 60 * 60 * 24),
    1
  );

  totalPrice.value = selectedCar.value.tarif * days;

  switch (payment.value.fuelLevel) {
    case '1/4':
      fuelPrice.value = 15;
      break;
    case '1/2':
      fuelPrice.value = 30;
      break;
    case '3/4':
      fuelPrice.value = 45;
      break;
    case 'Plein':
      fuelPrice.value = 60;
      break;
    default:
      fuelPrice.value = 0;
  }
};

// Update prices when fuel level changes
const handleFuelLevelChange = () => {
  calculatePrices();
};

// Watch fuel level for changes and recalculate price
watch(() => payment.value.fuelLevel, handleFuelLevelChange);

const openBookingModal = (car) => {
  selectedCar.value = car;
  payment.value.fuelLevel = '';
  showBookingModal.value = true;
  calculatePrices(); // Calculate prices when opening the booking modal

};

const closeBookingModal = () => {
  showBookingModal.value = false;
};

const handlePayment = async () => {
  closeBookingModal();
}
const handlePaymentOnline = async () => {
  alertMessage.value = "Sorry, Online payment not available at the moment";
alertDuration.value = 2000; // Set alert duration to 2 seconds
showAlert.value = true;
  closeBookingModal();
}

const handlePaymentPlus = async () => {
  // Extract email from local storage
  const email = localStorage.getItem('email');

  if (!email) {
    showBookingModal.value = false;

alertMessage.value = "You need to login first.";
alertDuration.value = 2000; // Set alert duration to 2 seconds
showAlert.value = true;

  setTimeout(() => {
    router.push('/login'); // Redirect to login after the alert duration
  }, 2000); // Adjust the delay (in milliseconds) to match your alert duration
  return;
}

  // Extract other details
  const car_id = selectedCar.value.id;
  const start_date = startDate.value;
  const end_date = endDate.value;
  const fuel_level = payment.value.fuelLevel;

  // Validate input data
  if (!email || !car_id || !start_date || !end_date) {
    alertMessage.value = "Please provide all required information (email, car, start date, end date).";
      alertDuration.value = 2000
    showAlert.value = true;
    return;
  }

  try {
    const response1 = await api.post('/users/getUser', { email });
     if (response1.data.user.category_id.length === 0) {
      alertMessage.value = "Your account is not verified, please complete your profile and wait for the admin to verify your account.";
      alertDuration.value = 2800

    showAlert.value = true;
      setTimeout(() => {
        router.push('/profile'); // Redirect to home after the alert is shown
      }, 3000); // Adjust the delay (in milliseconds) as needed        } else {
      return;
    } 
  
    // Make POST request to the backend endpoint

    const response = await api.post('/contracts/create', {
      email,
      car_id,
      start_date,
      end_date,
      fuel_level,
    });
  
    if (response.status == 200) {
      alertMessage.value = "Contract created successfully!";
    showAlert.value = true;
    setTimeout(() => {
        router.push('/contracts'); // Redirect to home after the alert is shown
      }, 2000); // Adjust the delay (in milliseconds) as needed        } else {
      // Handle more informative response if needed
    }
  } catch (error) {
    console.error(error);
  } finally {
    closeBookingModal();
  }
};
// Computed property to filter cars based on the search query
const filteredCars = computed(() => {
  if (!searchQuery.value) return cars.value;

  return cars.value.filter((car) => {
    const query = searchQuery.value.toLowerCase();
    if (searchType.value === 'price') {
      return car.tarif.toString().includes(query);
    } else if (searchType.value === 'model') {
      return extractCarName(car.name).toLowerCase().includes(query);
    } else {
      return (
        car.name.toLowerCase().includes(query) ||
        car.model.toLowerCase().includes(query) ||
        car.tarif.toString().includes(query)
      );
    }
  });
});


</script>

<style scoped>
.search-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
  justify-content: center;
}

.search-bar {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  flex: 1;
}

.search-type {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  min-width: 150px;
  background-color: #fff;
}

.search-type:focus {
  outline: none;
  border-color: #007bff;
}



/* General Styling */
.search-results {
  max-width: 1200px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.results-title {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 20px;
}

.date-range {
  text-align: center;
  font-size: 1rem;
  margin-bottom: 20px;
}

.loading-text,
.error-text,
.no-results {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 20px;
}

.car-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.car-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s;
}

.car-card:hover {
  transform: scale(1.05);
}

.car-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.car-info {
  padding: 15px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  display: flex;
  gap: 20px;
  background: white;
  width: 80%;
  max-width: 800px;
  padding: 20px;
  border-radius: 8px;
}

.modal-left {
  flex: 1;
}

.car-image-large {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.modal-right {
  flex: 1;
}

.payment-form .form-group {
  margin-bottom: 15px;
}

.payment-form input {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.payment-form select.fuel-level-dropdown {
  width: 100%;
  padding: 12px;
  border-radius: 4px;
  border: 2px solid #007bff;
  background-color: #f9f9f9;
  font-size: 1rem;
  color: #213363;
  margin-top: 10px;
  transition: border-color 0.3s ease;
}

.payment-form select.fuel-level-dropdown:focus {
  border-color: #0056b3;
}

.payment-logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin: 15px 0;
}

.payment-logos img {
  width: 50px;
  height: auto;
  display: block;
}

.modal-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  padding: 10px 0;
  border-top: 1px solid #ddd;
}

.modal-actions button {
  padding: 12px 24px;
  border: 2px solid #ddd;
  border-radius: 25px;
  background-color: transparent;
  color: #213363;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  flex: none;
  text-align: center;
}

.modal-actions button:hover {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.modal-actions button:active {
  background-color: #0056b3;
  border-color: #0056b3;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: scale(1);
}

@media (max-width: 768px) {
  .car-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }

  .car-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    cursor: pointer;
  }

  .car-card:hover {
    transform: scale(1.05);
  }

  .car-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
  }

  .car-info {
    padding: 15px;
    text-align: center;
  }

  .car-name {
    font-size: 1.5rem;
    font-weight: bold;
    color: #213363;
  }

  .car-description {
    font-size: 1rem;
    color: #555;
  }

  .car-price {
    font-size: 1.2rem;
    color: #28a745;
    font-weight: bold;
  }
}
</style>
