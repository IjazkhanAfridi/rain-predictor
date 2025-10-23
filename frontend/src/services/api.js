import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const signup = async (email, password) => {
  try {
    const response = await api.post('/signup/', { email, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || { success: false, error: 'Signup failed' };
  }
};

export const login = async (email, password) => {
  try {
    const response = await api.post('/login/', { email, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || { success: false, error: 'Login failed' };
  }
};

export const makePrediction = async (location, date) => {
  try {
    const response = await api.post('/predict/', { location, date });
    return response.data;
  } catch (error) {
    throw error.response?.data || { success: false, error: 'Prediction failed' };
  }
};

export const getHistory = async () => {
  try {
    const response = await api.get('/history/');
    return response.data;
  } catch (error) {
    throw error.response?.data || { success: false, error: 'Failed to fetch history' };
  }
};

export const getUserProfile = async () => {
  try {
    const response = await api.get('/profile/');
    return response.data;
  } catch (error) {
    throw error.response?.data || { success: false, error: 'Failed to fetch profile' };
  }
};

export default api;
