<template>
  <div class="card">
    <h1>🔐 Create Account</h1>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" maxlength="50" required />
      <button type="submit">Register</button>
    </form>
    <p>Have an account? <router-link to="/">Login</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')

const register = async () => {
  try {
    const res = await axios.post('http://localhost:5000/register', null, {
      params: { username: username.value, password: password.value }
    })
    localStorage.setItem('userId', res.data.id)
    localStorage.setItem('username', username.value)
    alert('✓ Account created!')
    router.push('/setup-2fa')
  } catch (err) {
    // Fixed error display
    const msg = err.response?.data?.detail || err.message || 'Registration failed'
    alert('Error: ' + msg)
  }
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  text-align: center;
}
h1 { margin-bottom: 30px; color: #333; }
input {
  width: 100%;
  padding: 15px;
  margin-bottom: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 15px;
}
input:focus {
  outline: none;
  border-color: #667eea;
}
button {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
button:hover { transform: translateY(-2px); }
p { margin-top: 20px; color: #666; }
a { color: #667eea; text-decoration: none; font-weight: 600; }
</style>
