import axios from 'axios';

// 1. Konfiguracja instancji (Base URL)
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Adres Twojego FastAPI
    headers: {
        'Content-Type': 'application/json',
    }
});

export default {
    // 2. Pobieranie listy dostępnych modeli
    // Backend: GET /models/
    getModels() {
        return apiClient.get('/models/');
    }
};