<template>
  <div class="profile-container">
    <h2 class="profile-title">
  My Profile
  <span 
    :class="[
      'verification-icon',
      profile.category_id?.length > 0 ? 'verified' : 'not-verified'
    ]"
    title="Verification status"
  >
    <i class="bi bi-patch-check"></i>
  </span>
</h2>

    <div v-if="profile" class="profile-view">
      <!-- Left Column: Personal Information -->
      <div class="profile-left">
        <section class="profile-section">
          <h3 class="section-title">Personal Information</h3>
          <div class="profile-field">
            <label class="field-label">Full Name:</label>
            <span class="field-value">{{ profile.name || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'name', label: 'Full Name', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Email Address:</label>
            <span class="field-value">{{ profile.email || 'Not provided' }}</span>
          </div>
          <div class="profile-field">
            <label class="field-label">Phone Number:</label>
            <span class="field-value">{{ profile.mobile || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'mobile', label: 'phone number', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Date of Birth:</label>
            <span class="field-value">{{ profile.x_date_of_birth || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'x_date_of_birth', label: 'Date of birth', type: 'date' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Place of Birth:</label>
            <span class="field-value">{{ profile.x_place_of_birth || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'x_place_of_birth', label: 'Place of birth', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Profile Picture:</label>
            <img v-if="profile.image_1920" :src="`data:image/png;base64,${profile.image_1920}`" class="profile-image-preview" />
            <span v-else>No image provided</span>
            <button @click="openEditModal({ key: 'image_1920', label: 'Profile Picture', type: 'file' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <!-- passwordh -->
          <div class="profile-field">
            <label class="field-label">Password:</label>
            <span class="field-value">**********</span>
            <button @click="openPasswordModal({ key: 'password', label: 'password', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
        </section>

        <!-- Identity Section -->
        <section class="profile-section">
          <h3 class="section-title">Identity</h3>
          <div class="profile-field">
            <label class="field-label">CIN Number:</label>
            <span class="field-value">{{ profile.cin_number || 'Not provided' }}</span>
          </div>
          <div class="profile-field">
            <label class="field-label">CIN Issue Date:</label>
            <span class="field-value">{{ profile.x_cin_issue_date || 'Not provided' }}</span>
          </div>
          <div class="profile-field">
            <label class="field-label">CIN Picture:</label>
            <img v-if="profile.identity_card_picture" :src="`data:image/png;base64,${profile.identity_card_picture}`"
              class="profile-image-preview" />
            <span v-else>No image provided</span>
            <button @click="openEditModal({ key: 'identity_card_picture', label: 'CIN Picture', type: 'file' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          
        </section>
      </div>

      <!-- Right Column -->
      <div class="profile-right">
        <section class="profile-section">
          <h3 class="section-title">Address Information</h3>
          <div class="profile-field">
            <label class="field-label">Street:</label>
            <span class="field-value">{{ profile.street || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'street', label: 'Street1', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Street 2:</label>
            <span class="field-value">{{ profile.street2 || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'Street2', label: 'Street2', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">City:</label>
            <span class="field-value">{{ profile.city || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'city', label: 'city', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Postal Code:</label>
            <span class="field-value">{{ profile.zip || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'zip', label: 'Postal Code', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Country:</label>
            <span class="field-value">{{ profile.country_id?.[1] || 'Not provided' }}</span>
          </div>
        </section>

        <!-- License Section -->
        <section class="profile-section">
          <h3 class="section-title">License</h3>
          <div class="profile-field">
            <label class="field-label">License Number:</label>
            <span class="field-value">{{ profile.driver_license_number || 'Not provided' }}</span>
          </div>
          <div class="profile-field">
            <label class="field-label">License Issue Date:</label>
            <span class="field-value">{{ profile.x_license_issue_date || 'Not provided' }}</span>
          </div>
          <div class="profile-field">
            <label class="field-label">License Category:</label>
            <span class="field-value">{{ profile.x_license_category || 'Not provided' }}</span>
            <button @click="openEditModal({ key: 'x_license_category', label: 'Licence category', type: 'text' })" class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
          <div class="profile-field">
            <label class="field-label">Driver License Picture:</label>
            <img v-if="profile.drivers_license_picture" :src="`data:image/png;base64,${profile.drivers_license_picture}`"
              class="profile-image-preview" />
            <span v-else>No image provided</span>
            <button @click="openEditModal({ key: 'drivers_license_picture', label: 'Licence Picture', type: 'file' })"
              class="edit-button">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </div>
        </section>
      </div>
    </div>

  <!-- Edit Field Modal -->
  <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="modal-title">Edit {{ currentField.label }}</h3>
        <input
          v-if="currentField.type === 'text'"
          v-model="editValue"
          type="text"
          class="modal-input"
        />
        <input
          v-if="currentField.type === 'date'"
          v-model="editValue"
          type="date"
          class="modal-input"
        />
        <input
          v-if="currentField.type === 'file'"
          type="file"
          @change="handleFileChange"
          class="modal-input"
        />
        <div class="modal-actions">
          <button @click="confirmEdit" class="save-button">Save</button>
          <button @click="closeEditModal" class="cancel-button">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showEditPasswordModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="modal-title">Change Password</h3>
        <input type="password" v-model="oldPassword" placeholder="Old Password" class="modal-input" />
        <input type="password" v-model="newPassword" placeholder="New Password" class="modal-input" />
        <input type="password" v-model="confirmNewPassword" placeholder="Confirm New Password" class="modal-input" />
        <div class="modal-actions">
          <button @click="confirmPasswordChange" class="save-button">Save</button>
          <button @click="closePasswordModal" class="cancel-button">Cancel</button>
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
import { ref, onMounted } from 'vue';
import api from '@/api';
import AlertModal from "./AlertModal.vue"; // Adjust path as needed



// Profile and Modal State
const profile = ref({});
const showEditModal = ref(false);
const modalField = ref('');
const currentField = ref('');

const modalLabel = ref('');
const modalType = ref('');
const editValue = ref('');
const newPassword = ref('');
const oldPassword = ref('');
const confirmNewPassword = ref('');
const showEditPasswordModal = ref(false);
const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(""); // Message to display in the alert modal


// Fetch Profile Data from API
const fetchProfile = async () => {
  try {
    const email = localStorage.getItem('email'); // Get email from localStorage
    if (!email) {
      alertMessage.value = "No email found in local storage";
      showAlert.value = true;
      return;
    }

    const response = await api.post('/users/getUser', { email });
    if (response) {

      profile.value = response.data.user; // Assuming the response contains the profile data
    }
  } catch (error) {
    console.error("Failed to fetch profile:", error);
    alertMessage.value = "Error fetching profile data.";
    showAlert.value = true;
  }
};

/* const openEditModal = (field, type) => {
  modalField.value = field; // Set the field to be edited
  modalLabel.value = field.replace(/_/g, ' ').toUpperCase(); // Generate a label for the modal
  modalType.value = type; // Set the input type (e.g., text, date, file)
  editValue.value = profile.value[field] || ''; // Set the current value for the field
  showEditModal.value = true; // Show the edit modal
}; */
// Open the edit modal for a specific field (excluding files)
const openEditModal = (field) => {
  currentField.value = field;  // Set the current field
  editValue.value = profile.value[field.key] || '';  // Set the current value for editing
  showEditModal.value = true;  // Show the edit modal
};


const handleFileChange = (event) => {
  const file = event.target.files[0]; // Get the selected file
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64String = e.target.result.split(",")[1]; // Extract Base64 string
      editValue.value = base64String; // Store the Base64 string
    };
    reader.onerror = (error) => {
      console.error("File read error:", error); // Debug: Handle file read errors
    };
    reader.readAsDataURL(file); // Read the file as a Base64 string
  } else {
    console.error("No file selected"); // Debug: Handle case when no file is selected
  }
};



// Confirm Edit and Update Profile
const confirmEdit = async () => {
  try {
    const data = {
      email: profile.value.email, // The email will be sent for identification
      [currentField.value.key]: editValue.value, // The field that was modified
    };


    // Send the data to update the user's profile
    const response = await api.post('/users/update', data);
    if (response.status === 200) {
      profile.value[currentField.value.key] = editValue.value; // Update local profile data
      alertMessage.value = `${currentField.value.label} updated successfully`;
    } else {
      alertMessage.value = response.data.error || "Failed to update profile.";
    }
    showAlert.value = true;
    showEditModal.value = false; // Close the modal after saving changes
  } catch (error) {
    alertMessage.value = "Failed to update profile.";
    showAlert.value = true;
    console.error(`Failed to update ${currentField.value.label}:`, error); // Debug: Log error details
  }
};



// Close the edit modal without saving
const closeEditModal = () => {
  showEditModal.value = false;  // Close the modal without saving
};
// Open the password modal
const openPasswordModal = (field) => {
  showEditPasswordModal.value = true;
};

// Close the password modal
const closePasswordModal = () => {
  showEditPasswordModal.value = false;
};

// Confirm and submit the password change
const confirmPasswordChange = async () => {
  if (newPassword.value !== confirmNewPassword.value) {
    alertMessage.value = "New passwords do not match";
    showAlert.value = true;
    return;
  }

  try {
    const data = {
      email: profile.value.email, // Send the email for identification
      oldPassword: oldPassword.value, // The old password
      newPassword: newPassword.value, // The new password
    };

    const response = await api.post('/users/password', data); // API endpoint for password update
    alertMessage.value = "Password updated successfully!";
    showAlert.value = true;
    closePasswordModal(); // Close the modal
  } catch (error) {
    console.error('Error updating password:', error);
    alertMessage.value = "Error updating password";
    showAlert.value = true;
  }
};

// Fetch profile data when component is mounted
onMounted(fetchProfile);
</script>


<style>
.profile-container {
  max-width: 100%;
  margin: 40px auto;
  padding: 30px;
  background-color: #fafafa;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.profile-title {
  font-size: 2.5rem;
  color: #213363;
  gap: 10px; /* Add spacing between text and icon */

  font-weight: 700;
  margin-bottom: 30px;
  text-align: center;
}


.verification-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%; /* Make it circular */
  margin-left: 10px; /* Spacing between title and icon */
  font-size: 1.5rem; /* Size of the icon */
  transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transitions */
}

/* Verified style: green background */
.verification-icon.verified {
  color:  #28a745; /* White icon color */
}


.profile-view {
  display: flex;
  justify-content: space-between;
  gap: 30px;
}

.profile-left,
.profile-right {
  width: 48%;
}

.profile-section {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #213363;
  margin-bottom: 15px;
}

.profile-field {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.field-label {
  font-weight: 600;
  color: #555;
  flex: 0.4;
}

.field-value {
  flex: 0.6;
  color: #333;
}

.edit-button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 1.2rem;
}

.edit-button:hover {
  color: #0056b3;
}

.profile-image-preview {
  max-width: 120px;
  max-height: 120px;
  border-radius: 8px;
  margin-right: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  width: 450px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal-input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.save-button,
.cancel-button {
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 48%;
  font-size: 1.1rem;
}

.save-button {
  background-color: #28a745;
  color: white;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
}
</style>
