<template>
  <div class="login-container">
    <div class="login-form">
      <h1>Books Management System</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input v-model="form.username" type="text" id="username" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="form.password" type="password" id="password" required />
        </div>
        <button type="submit" class="btn-login">Login</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
      <p class="register-link">
        Don't have an account? <a href="#" @click="showRegister = true">Register here</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/bookService'

const form = ref({ username: '', password: '' })
const error = ref('')
const router = useRouter()
const showRegister = ref(false)

const handleLogin = async () => {
  try {
    const response = await authService.login(form.value.username, form.value.password)
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data))
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.btn-login {
  width: 100%;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

.btn-login:hover {
  background: #5568d3;
}

.error {
  color: #e74c3c;
  margin-top: 15px;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  cursor: pointer;
}
</style>
