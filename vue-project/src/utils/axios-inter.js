import axios from 'axios';
import router from '../router';

// Création d'une instance axios avec une configuration de base
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

// Intercepteur pour ajouter le token à chaque requête
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les réponses et les erreurs
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Si l'erreur est 401 et que nous n'avons pas encore essayé de rafraîchir le token
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Tentative de rafraîchissement du token
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          // Si pas de refresh token, redirection vers login
          localStorage.clear();
          router.push('/login');
          return Promise.reject(error);
        }
        
        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refreshToken
        });
        
        // Stockage du nouveau token
        if (response.data.access) {
          localStorage.setItem('token', response.data.access);
          // Mise à jour du header de la requête originale avec le nouveau token
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return axiosInstance(originalRequest); // Réessai avec le nouveau token
        }
      } catch (refreshError) {
        // En cas d'échec du rafraîchissement, déconnexion et redirection
        localStorage.clear();
        router.push('/login');
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default axiosInstance;