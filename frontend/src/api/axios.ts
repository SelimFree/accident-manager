import axios, { isAxiosError } from 'axios'
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

export const getErrorMessage = (error: unknown) => {
  if (isAxiosError(error)) {
    if (error.response?.status === 409) {
      return 'This email is already registered.'
    }
    if (error.response?.status === 422) {
      return 'Please check your details: name 2-80 characters, a valid email, password 10-128 characters.'
    }
  }
  return 'Registration failed. Please try again.'
}
