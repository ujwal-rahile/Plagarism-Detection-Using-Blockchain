
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const loginUser = async (passkey) => {
    try {
        const response = await api.post('/login', { passkey });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : { error: "Network Error" };
    }
};

export const uploadFile = async (file, senderAddress) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('sender', senderAddress); // Backend expects 'sender'

    try {
        const response = await api.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : { error: "Network Error" };
    }
};

export default api;
