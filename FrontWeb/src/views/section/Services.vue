<template>
    <section id="services" class="relative bg-gray-50 my-4 md:my-10 mx-1 md:mx-4 font-poppins">
        <div class="container px-4 my-4 md:my-10 py-8 lg:max-w-screen-xl lg:px-8 mx-auto text-gray-700 relative">
            <!-- Header Section -->
            <div class="py-3 mx-2 sm:max-w-xl md:max-w-full lg:max-w-screen-xl lg:py-6 relative sm:mx-auto">
                <div class="clip absolute top-4 left-0 md:block hidden">
                    <div class="flex flex-row items-center">
                        <svg class="w-14" viewBox="0 0 60 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M11.3418 0H32L20.2532 52H0L11.3418 0Z" fill="#00FF29" />
                            <path d="M39.3418 0H60L48.2532 52H28L39.3418 0Z" fill="white" />
                        </svg>
                        <hr class="border border-gray-200 w-[16rem] mx-2">
                    </div>
                </div>
                <div class="clip absolute top-4 right-0 md:block hidden">
                    <div class="flex flex-row-reverse items-center">
                        <svg width="60" height="52" viewBox="0 0 60 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M11.3418 0H32L20.2532 52H0L11.3418 0Z" fill="#00FF29" />
                            <path d="M39.3418 0H60L48.2532 52H28L39.3418 0Z" fill="white" class="shadow-lg" />
                        </svg>
                        <hr class="border border-gray-200 w-[16rem] mx-2">
                    </div>
                </div>
                <div class="relative">
                    <div class="title mb-2 md:mb-6 text-center">
                        <h2 data-aos="fade-up"
                            class="mb-2 font-rubik text-xl font-bold tracking-tight text-sky-950 sm:text-4xl sm:leading-none">
                            Explore Offers
                        </h2>
                    </div>
                    <div class="desc w-full md:w-1/2 mx-auto">
                        <p data-aos="fade-down"
                            class="mb-2 text-sm md:text-lg font-normal leading-relaxed font-roboto text-center text-sky-950">
                            Discover our wide range of offers designed to provide the best solutions for your mobility
                            needs, featuring a fleet
                            of high-quality vehicles.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Dynamic Car List -->
            <div class="md:gap-10 sm:mx-8 lg:mx-auto lg:grid-cols-3 lg:max-w-screen-xl grid grid-cols-2 gap-2 mx-2">
                <!-- Loading State -->
                <div v-if="cars.length === 0 && !loading && !error" class="col-span-full text-center py-6">
                    <p class="text-sky-900 font-medium text-lg">No cars available for the selected dates.</p>
                </div>

                <!-- Loading Spinner -->
                <div v-if="loading" class="col-span-full text-center py-6">
                    <p class="text-sky-900 font-medium text-lg">Loading cars... Please wait.</p>
                </div>

                <!-- Error State -->
                <div v-if="error" class="col-span-full text-center py-6">
                    <p class="text-red-500 font-medium text-lg">Error fetching cars. Please try again later.</p>
                </div>

                <!-- Dynamic Car Cards -->
                <div v-for="car in cars" :key="car.id" data-aos="zoom-in"
                    class="rounded-md bg-slate-100 border-dotted border-[3px] border-sky-800">
                    <div class="relative mb-4 rounded shadow">
                        <img class="object-cover rounded" width="400" height="400"
                            :src="car.image || '/assets/default_car_image.jpg'" :alt="car.name || 'Car Image'" />
                    </div>
                    <div class="font-poppins flex flex-col gap-4 text-center">
                        <p class="text-base md:text-lg font-bold text-sky-900 uppercase">
                            {{ extractCarName(car.name) || 'Unnamed Car' }}
                        </p>
                        <p class="mb-2 text-xs font-semibold text-sky-900 capitalize">
                            {{ car.tarif || 'N/A' }} TND
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api'; // Replace with your actual API import or axios instance


const cars = ref([]); // Array to store available cars
const loading = ref(true); // Loading state
const error = ref(false); // Error state

const extractCarName = (fullName) => {
    const parts = fullName.split('/');
    return parts.length >= 2 ? `${parts[0]}/${parts[1]}` : fullName;
};
// Fetch cars from the API
const fetchCars = async () => {
    try {
        const response = await api.post('/vehicles/available', {
            start_date: '2029-12-07',
            end_date: '2029-12-08',

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
        console.error('Error fetching cars:', err);
        error.value = true;
        loading.value = false;
    }
};

// Call the fetchCars function on component mount
onMounted(fetchCars);

</script>
