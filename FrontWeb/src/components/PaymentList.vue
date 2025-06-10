<template>
  <div class="payment-list-container">
    <h1 class="payment-title">Payment List</h1>
    <!-- Search Bar -->
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search payments..."
      class="search-bar"
    />
    <!-- Payment Table -->
    <div class="table-wrapper">
      <table class="payment-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Contract</th>
            <th>Amount No Tax</th>
            <th>Total Amount Paid</th>
            <th>Date of Payment</th>
          </tr>
        </thead>
        <tbody>
          <!-- Iterate through filtered payments -->
          <tr v-for="payment in filteredPayments" :key="payment.id">
            <td>{{ payment.name !== '/' ? payment.name : 'Not Paid' }}</td>

            <td>{{ payment.contract }}</td>
            <td>{{ payment.amount_notax }}</td>
            <td>{{ payment.amount_total }}</td>
            <td>{{ payment.date }}</td>            
          </tr>
        </tbody>
      </table>
    </div>
    <AlertModal
      :message="alertMessage"
      :visible="showAlert"
      @close="showAlert = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/api';
import AlertModal from "./AlertModal.vue"; // Adjust path as needed
const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(""); // Message to display in the alert modal

const payments = ref([]);
const searchQuery = ref('');

// Fetch payments based on the email stored in local storage
const fetchPayments = async () => {
  const email = localStorage.getItem('email');
  if (!email) {
    alertMessage.value = "Email not found in local storage.";
    showAlert.value = true;    return;
  }

  try {
    const response = await api.post('/payments/email', { email });
    payments.value = response.data.result.Payments; // Assuming payments are returned in the response under 'payments' key
  } catch (error) {
    console.error('Failed to fetch payments:', error);
    alertMessage.value = "Failed to fetch payments. Please try again later.";
    showAlert.value = true;  }
};

onMounted(() => {
  fetchPayments();
});

// Computed property for filtering payments based on search query
const filteredPayments = computed(() =>
  payments.value.filter(payment =>
    Object.values(payment)
      .join(' ')
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase())
  )
);

</script>

<style scoped>
/* Styles for Payment List */
.payment-list-container {
  max-width: 1000px;
  margin: 50px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.payment-title {
  text-align: center;
  font-size: 2.2rem;
  font-weight: bold;
  color: #213363;
  margin-bottom: 20px;
}

.search-bar {
  width: 100%;
  padding: 12px 16px;
  margin-bottom: 25px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search-bar:focus {
  border-color: #007bff;
  box-shadow: 0 0 6px rgba(0, 123, 255, 0.8);
}

.table-wrapper {
  overflow-x: auto;
}

.payment-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.payment-table th,
.payment-table td {
  text-align: left;
  padding: 16px;
  border: 1px solid #ddd;
  font-size: 1rem;
}

.payment-table th {
  background-color: #f1f4f9;
  color: #333;
  font-weight: bold;
  text-transform: uppercase;
}

.payment-table tr:nth-child(even) {
  background-color: #fafafa;
}

.payment-table tr:hover {
  background-color: #eef2f7;
}

.status-completed {
  color: #28a745;
  font-weight: bold;
}

.status-pending {
  color: #ffc107;
  font-weight: bold;
}

.print-receipt-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  font-size: 1.2rem;
  color: #fff;
  background-color: #6c757d;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.print-receipt-button:hover {
  background-color: #5a6268;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-3px);
}

.print-receipt-button:active {
  background-color: #545b62;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .payment-title {
    font-size: 1.8rem;
  }

  .payment-table th,
  .payment-table td {
    padding: 12px;
    font-size: 0.9rem;
  }

  .print-receipt-button {
    font-size: 1rem;
    padding: 8px;
  }
}

@media (max-width: 480px) {
  .payment-list-container {
    padding: 15px;
  }

  .search-bar {
    font-size: 0.9rem;
    padding: 10px;
  }

  .payment-table th,
  .payment-table td {
    padding: 10px;
    font-size: 0.85rem;
  }
}
</style>
