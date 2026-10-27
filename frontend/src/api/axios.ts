import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const publicApi = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
})


export const privateApi = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
})

privateApi.interceptors.request.use((config) => {
    const token = useAuthStore.getState().token

    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

privateApi.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            useAuthStore.getState().logout()
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)