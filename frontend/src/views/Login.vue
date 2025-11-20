<template>
  <div class="card">
    <h1>👋 Welcome Back</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-if="requires2FA" v-model="token" placeholder="6-digit code" maxlength="6" />
      <button type="submit">{{ requires2FA ? 'Verify' : 'Login' }}</button>
    </form>
    <p>No account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')
const token = ref('')
const requires2FA = ref(false)
const userId = ref(null)

const login = async () => {
  try {
    if (!requires2FA.value) {
      const res = await axios.post('http://localhost:5000/login', null, {
        params: { username: username.value, password: password.value }
      })
      userId.value = res.data.user_id
      requires2FA.value = res.data.requires_2fa
      
      if (!requires2FA.value) {
        alert('Please set up 2FA first')
      }
    } else {
      await axios.post('http://localhost:5000/2fa/verify', null, {
        params: { user_id: userId.value, code: token.value }
      })
      alert('✓ Login successful!')
    }
  } catch (err) {
    const msg = err.response?.data?.detail || err.message || 'Login failed'
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
