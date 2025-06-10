// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/section/Home.vue';
import About from '@/views/section/About.vue';
import Services from '@/views/section/Services.vue';
import Contact from '@/views/section/Contact.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import AppLayout from '@/components/AppLayout.vue';
import Profile from '@/components/Profile.vue';
import Search from '@/components/Search.vue';


const routes = [
    {
      path: '/',
      component: AppLayout, // Use AppLayout as the main wrapper
      children: [
        { path: '', name: 'Home', component: Home },
        { path: 'about', name: 'About', component: About },

        { path: 'services', name: 'Services', component: Services },
        { path: 'contact', name: 'Contact', component: Contact },
      ]
    },
    { path: '/profile', component: Profile, meta: { requiresAuth: true } },

    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },
    {path: '/search',
    name: 'Search',
    component: Search,},
    {
      path: '/contracts',
      name: 'Contracts',
      component: () => import('@/components/ContractList.vue')
    },
    {
      path: '/payments',
      name: 'Payments',
      component: () => import('@/components/PaymentList.vue')
    }

  ];
  
  const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
      if (savedPosition) {
        return savedPosition;
      } else if (to.hash) {
        return {
          el: to.hash,
          behavior: 'smooth',
        };
      } else {
        return { top: 0 };
      }
    }
  });
  
export default router;


