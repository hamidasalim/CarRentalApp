<template>
    <section id="contact" class="relative lg:py-10 bg-gray-50 mx-4">
      <div class="px-4 py-6 mx-auto sm:max-w-xl md:max-w-full lg:max-w-screen-lg md:px-24 lg:px-8">
        <div class="relative max-w-2xl sm:mx-auto sm:max-w-xl md:max-w-2xl text-center">
          <h2
            data-aos="fade-up"
            class="mb-6 font-rubik text-xl font-bold tracking-tight text-sky-900 sm:text-4xl sm:leading-none"
          >
            Build Communication, Realize Your Dream Journey: Contact Us
          </h2>
          <p data-aos="fade-down" class="mb-6 text-base font-roboto text-sky-800">
            We are ready to provide the assistance you need, ensuring every detail
            of your trip with
            <span class="font-semibold">Hamida's Rentals</span> is unforgettable.
          </p>
        </div>
      </div>
      <div
        class="flex flex-col items-center justify-between lg:p-10 mx-auto sm:max-w-xl md:max-w-full lg:max-w-screen-xl xl:px-5 lg:flex-row"
      >
        <div class="flex flex-col items-center w-full py-8 px-6 lg:flex-row bg-sky-900 rounded-[2rem] gap-6">
          <div class="w-full relative max-w-md lg:max-w-2xl lg:w-6/12 px-2 md:px-4">
            <iframe
              src="https://maps.app.goo.gl/QV9N9JBmTWBFa32EA"
              loading="lazy"
              class="rounded-lg md:h-[31.25rem] h-80 w-full"
            ></iframe>
          </div>
          <div
            class="w-full relative z-10 max-w-2xl lg:mt-0 lg:w-5/12 px-2 md:px-4"
          >
            <div
              data-aos="zoom-in-left"
              data-aos-offset="200"
              data-aos-delay="200"
              class="flex flex-col items-start m-0 justify-start p-4 bg-white shadow-2xl rounded-xl relative"
            >
              <form @submit.prevent="sendEmail" class="w-full z-50">
                <p class="w-full lg:text-3xl text-xl font-medium text-center leading-snug font-poppins">
                  Leave your message
                </p>
                <div class="w-full mt-6 mx-0 mb-0 relative space-y-8">
                  <div class="relative">
                    <label
                      for="name"
                      class="bg-white py-0 px-2 -mt-3 mr-0 mb-0 ml-2 font-medium text-gray-600 absolute"
                      >Full Name</label
                    >
                    <input
                      v-model="name"
                      placeholder="John"
                      id="name"
                      type="text"
                      class="border placeholder-gray-400 p-2 focus:outline-none focus:border-black w-full lg:p-4 mt-2 mx-0 mb-0 text-base block bg-white border-gray-300 rounded-md"
                      required
                    />
                  </div>
                  <div class="relative">
                    <label
                      for="email"
                      class="bg-white py-0 px-2 -mt-3 mr-0 mb-0 ml-2 font-medium text-gray-600 absolute"
                      >Email</label
                    >
                    <input
                      v-model="email"
                      placeholder="name@mail.com"
                      id="email"
                      type="email"
                      class="border placeholder-gray-400 p-2 focus:outline-none focus:border-black w-full lg:p-4 mt-2 mx-0 mb-0 text-base block bg-white border-gray-300 rounded-md"
                      required
                    />
                  </div>
                  <div class="relative">
                    <label
                      for="message"
                      class="bg-white py-0 px-2 -mt-3 mr-0 mb-0 ml-2 font-medium text-gray-600 absolute"
                      >Message</label
                    >
                    <textarea
                      v-model="message"
                      placeholder="Your Message"
                      id="message"
                      class="border placeholder-gray-500 focus:outline-none focus:border-black w-full pt-4 lg:px-4 pb-4 px-2 mt-2 mx-0 text-base block bg-white border-gray-300 rounded-md"
                      required
                    ></textarea>
                  </div>
                  <div class="relative">
                    <button
                      title="Send Message"
                      type="submit"
                      class="w-full inline-block pt-4 pr-5 pb-4 pl-5 text-xl cursor-pointer font-medium text-center text-white bg-green-400 rounded-lg transition duration-200 hover:bg-green-600 ease"
                    >
                      Send
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
        <AlertModal
      :message="alertMessage"
      :visible="showAlert"
      @close="showAlert = false"
    />
      </div>
    </section>
  </template>
<script setup>
import { ref } from "vue";
import axios from "axios";
import AlertModal from "../../components/AlertModal.vue"; // Adjust path as needed
const showAlert = ref(false); // State to show or hide the alert modal
const alertMessage = ref(""); // Message to display in the alert modal

// Form data
const name = ref("");
const email = ref("");
const message = ref("");

// Send email function
const sendEmail = async () => {
  try {
    const response = await axios.post("http://vps-570f1122.vps.ovh.net:3000/api/send-email", {
      name: name.value,
      email: email.value,
      message: message.value,
    });
    alertMessage.value = "Your message has been sent successfully!";
    showAlert.value = true;
    // Clear the form
    name.value = "";
    email.value = "";
    message.value = "";
  } catch (error) {
    console.error("Failed to send email:", error);
    alertMessage.value = "Failed to send your message. Please try again later..";
    showAlert.value = true;
  }
};
</script>
<style scoped>
    .floating {
        animation-name: floating;
        animation-duration: 3s;
        animation-iteration-count: infinite;
        animation-timing-function: ease-in-out;
    }

    @keyframes floating {
        0% {
            transform: translate(0, 0px);
        }

        50% {
            transform: translate(0, 8px);
        }

        100% {
            transform: translate(0, -0px);
        }
    }

    .floating-4 {
        animation-name: floating;
        animation-duration: 4s;
        animation-iteration-count: infinite;
        animation-timing-function: ease-in-out;
    }

    @keyframes floating-4 {
        0% {
            transform: translate(0, 0px);
        }

        50% {
            transform: translate(0, 8px);
        }

        100% {
            transform: translate(0, -0px);
        }
    }

</style>