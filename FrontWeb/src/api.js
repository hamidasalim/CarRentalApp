// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://vps-570f1122.vps.ovh.net:3000/api',
  //baseURL: 'http://localhost:3000/api',

  headers: {
      'Content-Type': 'application/json',
  },
  withCredentials: true,
});


// Add JWT token to request headers if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
