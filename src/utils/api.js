import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const login = async (account_number, pin) => {
  try {
    const response = await api.post('/login', { account_number, pin })
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const getBalance = async (account_number) => {
  try {
    const response = await api.get(`/balance/${account_number}`)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const withdraw = async (account_number, amount) => {
  try {
    const response = await api.post('/withdraw', { account_number, amount })
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const deposit = async (account_number, amount) => {
  try {
    const response = await api.post('/deposit', { account_number, amount })
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export default {
  login,
  getBalance,
  withdraw,
  deposit
}
