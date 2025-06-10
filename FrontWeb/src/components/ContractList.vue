<template>
  <div class="contract-list-container">
    <h1 class="contract-title">Contract List</h1>
    <input type="text" v-model="searchQuery" placeholder="Search contracts..." class="search-bar" />
    <table class="contract-table">
      <thead>
        <tr>
          <th>Contract </th>
          <th>Car</th>
          <th>Start Date</th>
          <th>End Date</th>
          <th>Status</th>
          <th>Total Price</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contract in filteredContracts" :key="contract.id">
          <td>{{ contract.name }}</td>
          <td>{{ contract.vehicle }}</td>
          <td>{{ contract.rent_start_date }}</td>
          <td>{{ contract.rent_end_date}}</td>
          <td>{{ contract.state}}</td>
          <td>{{ contract.total_cost}}</td>
          
          <td v-if="contract.state !== 'cancel'">
            <button @click="openCancelModal(contract)" class="action-button">
              Cancel Reservation
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal for Cancel Confirmation -->
    <div v-if="showCancelModal" class="modal-overlay">
      <div class="modal-content">
        <h2 class="modal-title">Cancel Reservation</h2>
        <p>
          Are you sure you want to cancel this reservation for
          <strong>{{ selectedContract.car }}</strong>?
        </p>
        <div class="modal-actions">
          <button @click="confirmCancel" class="confirm-button">Yes, Cancel</button>
          <button @click="closeCancelModal" class="cancel-button">No, Go Back</button>
        </div>
      </div>
    </div>
    <AlertModal
      :message="alertMessage"
      :visible="showAlert"
      @close="showAlert = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import AlertModal from "./AlertModal.vue"; // Adjust path as needed
const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(""); // Message to display in the alert modal

const contracts = ref([]);
const showCancelModal = ref(false);
const selectedContract = ref({});
const searchQuery = ref('');

// Fetch contracts based on the email stored in local storage
const fetchContracts = async () => {
  const email = localStorage.getItem('email');
  if (!email) {
    alertMessage.value = 'Email not found in local storage.';
    showAlert.value = true;    return;
  }

  try {
    const response = await api.post('/contracts/email', { email });
    contracts.value = response.data.result.contracts; // Assuming contracts are returned in the response under 'contracts' key
  } catch (error) {
    console.error('Failed to fetch contracts:', error);
alertMessage.value = 'Failed to fetch contracts. Please try again later.';
showAlert.value = true;  }
};

onMounted(() => {
  fetchContracts();
});

// Computed property for filtering contracts based on search query
const filteredContracts = computed(() => {
  return contracts.value.filter(contract =>
    Object.values(contract)
      .join(' ')
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase())
  );
});

const openCancelModal = (contract) => {
  selectedContract.value = contract;
  showCancelModal.value = true;
};

const closeCancelModal = () => {
  showCancelModal.value = false;
};

const confirmCancel = async () => {
  const email = localStorage.getItem('email');
  if (!email) {
    alertMessage.value = 'Email not found in local storage.';
    showAlert.value = true;    return;
  }

  try {
    const response = await api.post('/contracts/cancel', {
      email,
      contract_id: selectedContract.value.id
    });
alertMessage.value = `Contract for ${selectedContract.value.vehicle} has been canceled.`;
showAlert.value = true;    closeCancelModal();
    fetchContracts(); // Refresh the contracts list after cancellation
  } catch (error) {
    console.error('Failed to cancel contract:', error);
    alertMessage.value = 'Failed to cancel contract. Please try again later.';
    showAlert.value = true;  }
};

</script>

<style scoped>
.search-bar {
  width: 100%;
  padding: 12px 16px;
  margin-bottom: 25px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  outline: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search-bar:focus {
  border-color: #007bff;
  box-shadow: 0 0 6px rgba(0, 123, 255, 0.8);
}

.contract-list-container {
  max-width: 1100px;
  margin: 60px auto;
  padding: 25px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.contract-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: #213363;
  margin-bottom: 30px;
}

.contract-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.contract-table th,
.contract-table td {
  text-align: left;
  padding: 16px;
  border: 1px solid #ddd;
  font-size: 1rem;
}

.contract-table th {
  background-color: #f1f4f9;
  color: #333;
  font-weight: bold;
  text-transform: uppercase;
}

.contract-table tr:nth-child(even) {
  background-color: #fafafa;
}

.contract-table tr:hover {
  background-color: #eef2f7;
}

.status-active {
  color: #28a745;
  font-weight: bold;
}

.status-completed {
  color: #007bff;
  font-weight: bold;
}

.status-pending {
  color: #ffc107;
  font-weight: bold;
}

.action-button {
  padding: 8px 14px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: #ffffff;
  padding: 30px;
  border-radius: 15px;
  width: 450px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 25px;
  color: #213363;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
}

.confirm-button,
.cancel-button {
  padding: 12px 25px;
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.confirm-button {
  background-color: #28a745;
}

.confirm-button:hover {
  background-color: #218838;
  transform: scale(1.05);
}

.cancel-button {
  background-color: #dc3545;
}

.cancel-button:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

/* Responsive Design */
@media (max-width: 768px) {
  .contract-list-container {
    margin: 80px auto;
    padding: 20px;
  }

  .contract-title {
    font-size: 2rem;
  }

  .modal-content {
    width: 90%;
  }
}
</style>
