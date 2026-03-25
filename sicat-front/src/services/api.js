import axios from 'axios'

const API_BASE_URL = 'http://localhost:7000'
const SUAP_API_URL = 'https://suap.ifrn.edu.br/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

const suapApi = axios.create({
  baseURL: SUAP_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_nome')
      window.dispatchEvent(new Event('auth-changed'))
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: async (matricula, senha) => {
    const response = await api.post('/api/auth/login', {
      matricula,
      senha
    })
    return response.data
  },
  
  validateSuap: async (matricula, senha_suap) => {
    try {
      const tokenResponse = await suapApi.post('/token/pair', {
        username: matricula,
        password: senha_suap
      })
      
      const { access } = tokenResponse.data
      
      const userResponse = await suapApi.get('/rh/eu/', {
        headers: {
          'Authorization': `Bearer ${access}`
        }
      })
      
      return {
        valido: true,
        token: access,
        dados: userResponse.data
      }
    } catch (error) {
      if (error.response?.status === 401) {
        throw new Error('Credenciais do SUAP inválidas')
      }
      throw error
    }
  },
  
  register: async (matricula, senha_suap, nova_senha, confirmar_senha) => {
    const response = await api.post('/api/auth/registro', {
      matricula,
      senha_suap,
      nova_senha,
      confirmar_senha
    })
    return response.data
  },
  
  getMe: async () => {
    const response = await api.get('/api/auth/perfil')
    return response.data
  }
}

export default api

