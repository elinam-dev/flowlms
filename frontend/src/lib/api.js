import axios from 'axios';

// Create a function to get the API URL dynamically
const getApiUrl = () => {
  let baseUrl = process.env.REACT_APP_BACKEND_URL || '';
  
  // Force HTTPS in production when accessed via HTTPS
  if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
    baseUrl = baseUrl.replace('http://', 'https://');
  }
  
  return `${baseUrl}/api`;
};

// Set up axios interceptor to fix URLs
axios.interceptors.request.use((config) => {
  if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
    if (config.url && config.url.startsWith('http://')) {
      config.url = config.url.replace('http://', 'https://');
    }
    if (config.baseURL && config.baseURL.startsWith('http://')) {
      config.baseURL = config.baseURL.replace('http://', 'https://');
    }
  }
  return config;
});

const API = getApiUrl();

// Auth APIs
export const authApi = {
  login: (data) => axios.post(`${API}/auth/login`, data),
  register: (data) => axios.post(`${API}/auth/register`, data),
  me: () => axios.get(`${API}/auth/me`),
};

// User APIs
export const userApi = {
  getProfile: () => axios.get(`${API}/users/profile`),
  updateProfile: (data) => axios.put(`${API}/users/profile`, null, { params: data }),
  checkIn: () => axios.post(`${API}/users/check-in`),
  getCheckInStatus: () => axios.get(`${API}/users/check-in/status`),
};

// Course APIs
export const courseApi = {
  getAll: () => axios.get(`${API}/courses`),
  getEnrolled: () => axios.get(`${API}/courses/enrolled`),
  getById: (id) => axios.get(`${API}/courses/${id}`),
  enroll: (courseId) => axios.post(`${API}/courses/enroll`, { course_id: courseId }),
};

// Progress APIs
export const progressApi = {
  updateLesson: (lessonId, completed) => axios.post(`${API}/progress/lesson`, { lesson_id: lessonId, completed }),
  getCourseProgress: (courseId) => axios.get(`${API}/progress/course/${courseId}`),
};

// Quiz APIs
export const quizApi = {
  getById: (id) => axios.get(`${API}/quizzes/${id}`),
  submit: (id, answers) => axios.post(`${API}/quizzes/${id}/submit`, { answers }),
};

// Certificate APIs
export const certificateApi = {
  getAll: () => axios.get(`${API}/certificates`),
  getById: (id) => axios.get(`${API}/certificates/${id}`),
  downloadPdf: (id) => axios.get(`${API}/certificates/${id}/pdf`, { responseType: 'blob' }),
};

// Admin APIs
export const adminApi = {
  getStats: () => axios.get(`${API}/admin/stats`),
  getUsers: () => axios.get(`${API}/admin/users`),
  createUser: (data) => axios.post(`${API}/admin/users`, data),
  deleteUser: (userId) => axios.delete(`${API}/admin/users/${userId}`),
  updateUserRole: (userId, role) => axios.post(`${API}/admin/users/${userId}/role`, null, { params: { role } }),
  
  // Courses
  createCourse: (data) => axios.post(`${API}/admin/courses`, data),
  updateCourse: (id, data) => axios.put(`${API}/admin/courses/${id}`, data),
  deleteCourse: (id) => axios.delete(`${API}/admin/courses/${id}`),
  assignCourse: (courseId, userIds) => axios.post(`${API}/admin/courses/${courseId}/assign`, userIds),
  getCourseProgress: (courseId) => axios.get(`${API}/admin/courses/${courseId}/progress`),
  
  // Modules
  createModule: (courseId, data) => axios.post(`${API}/admin/courses/${courseId}/modules`, data),
  updateModule: (id, data) => axios.put(`${API}/admin/modules/${id}`, data),
  deleteModule: (id) => axios.delete(`${API}/admin/modules/${id}`),
  
  // Lessons
  createLesson: (moduleId, data) => axios.post(`${API}/admin/modules/${moduleId}/lessons`, data),
  updateLesson: (id, data) => axios.put(`${API}/admin/lessons/${id}`, data),
  deleteLesson: (id) => axios.delete(`${API}/admin/lessons/${id}`),
  
  // Quizzes
  createQuiz: (moduleId, data) => axios.post(`${API}/admin/modules/${moduleId}/quizzes`, data),
  updateQuiz: (id, data) => axios.put(`${API}/admin/quizzes/${id}`, data),
  deleteQuiz: (id) => axios.delete(`${API}/admin/quizzes/${id}`),
};

// Upload APIs
export const uploadApi = {
  video: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API}/upload/video`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  document: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API}/upload/document`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  image: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API}/upload/image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
};
