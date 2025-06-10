<template>
    <div v-if="visible" class="alert-overlay">
      <div class="alert-content">
        <p>{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AlertModal",
    props: {
      message: {
        type: String,
        required: true,
      },
      visible: {
        type: Boolean,
        required: true,
      },
      duration: {
        type: Number,
        default: 1500, // Default auto-close duration: 2 seconds
      },
    },
    watch: {
      visible(newValue) {
        if (newValue) {
          setTimeout(() => {
            this.$emit("close");
          }, this.duration);
        }
      },
    },
  };
  </script>
  
  <style scoped>
.alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* Darker semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100; /* Ensure it appears above other modals */
}

/* Alert Modal Content */
.alert-content {
  background: linear-gradient(135deg, #ff7eb3, #ff758c); /* Gradient background */
  padding: 25px 40px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3); /* Stronger shadow */
  text-align: center;
  font-family: 'Arial', sans-serif;
  animation: slideDown 0.4s ease-out; /* Slide-down appearance */
  min-width: 350px;
  color: #ffffff; /* White text */
  z-index: 1200; /* Ensure content stays above other elements */
}

/* Alert Text */
.alert-content p {
  margin: 0;
  padding: 10px 0;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.5;
  color: #ffffff; /* Bright text for readability */
}

/* Animation */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


  </style>
  