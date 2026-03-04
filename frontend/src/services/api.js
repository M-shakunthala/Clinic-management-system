import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth services
export const authService = {
  login: async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  getCurrentUser: () => api.get('/me'),
  
  register: (userData) => api.post('/users', userData),
};

// Doctor services
export const doctorService = {
  getAll: (skip = 0, limit = 10) => api.get(`/doctors?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/doctors/${id}`),
  create: (doctorData) => api.post('/doctors', doctorData),
};

// Patient services
export const patientService = {
  getAll: (skip = 0, limit = 10) => api.get(`/patients?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/patients/${id}`),
  create: (patientData) => api.post('/patients', patientData),
};

// Appointment services
export const appointmentService = {
  getAll: (skip = 0, limit = 10) => api.get(`/appointments?skip=${skip}&limit=${limit}`),
  getById: (id) => api.get(`/appointments/${id}`),
  create: (appointmentData) => api.post('/appointments', appointmentData),
  getMyAppointments: (skip = 0, limit = 10) => api.get(`/my-appointments?skip=${skip}&limit=${limit}`),
};

// Medical record services
export const medicalRecordService = {
  getAll: (skip = 0, limit = 10, patientId = null) => {
    let url = `/medical-records?skip=${skip}&limit=${limit}`;
    if (patientId) url += `&patient_id=${patientId}`;
    return api.get(url);
  },
  getById: (id) => api.get(`/medical-records/${id}`),
  create: (recordData) => api.post('/medical-records', recordData),
};

// Combined API service for easier imports
export const apiService = {
  // Appointments
  getAppointments: () => api.get('/appointments'),
  getAppointment: (id) => api.get(`/appointments/${id}`),
  createAppointment: (appointmentData) => api.post('/appointments', appointmentData),
  updateAppointment: (id, data) => api.put(`/appointments/${id}`, data),
  deleteAppointment: (id) => api.delete(`/appointments/${id}`),
  
  // Patients
  getPatients: () => api.get('/patients'),
  getPatient: (id) => api.get(`/patients/${id}`),
  createPatient: (patientData) => api.post('/patients', patientData),
  updatePatient: (id, data) => api.put(`/patients/${id}`, data),
  deletePatient: (id) => api.delete(`/patients/${id}`),
  
  // Doctors
  getDoctors: () => api.get('/doctors'),
  getDoctor: (id) => api.get(`/doctors/${id}`),
  createDoctor: (doctorData) => api.post('/doctors', doctorData),
  updateDoctor: (id, data) => api.put(`/doctors/${id}`, data),
  deleteDoctor: (id) => api.delete(`/doctors/${id}`),
  
  // Medical Records
  getMedicalRecords: (skip = 0, limit = 10, patientId = null) => {
    let url = `/medical-records?skip=${skip}&limit=${limit}`;
    if (patientId) url += `&patient_id=${patientId}`;
    return api.get(url);
  },
  getMedicalRecord: (id) => api.get(`/medical-records/${id}`),
  createMedicalRecord: (recordData) => api.post('/medical-records', recordData),
};

export default api;
