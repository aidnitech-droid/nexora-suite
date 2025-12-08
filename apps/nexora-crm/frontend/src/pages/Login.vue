<template>
  <div class="login-container">
    <div class="login-form">
      <h1>Module Management</h1>
      <form @submit.prevent="handleLogin">
        <input v-model="form.username" type="text" placeholder="Username" required />
        <input v-model="form.password" type="password" placeholder="Password" required />
        <button type="submit" class="btn-login">Login</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/itemService'

const form = ref({ username: '', password: '' })
const error = ref('')
const router = useRouter()

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
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.btn-login {
  width: 100%;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error {
  color: #e74c3c;
  margin-top: 15px;
}
</style>
