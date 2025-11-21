<template>
  <div class="card">
    <h1>🔐 Setup 2FA</h1>
    <p class="subtitle">Scan with Google Authenticator</p>
    <img v-if="qrCode" :src="qrCode" class="qr" />
    <p class="secret" v-if="secret">Secret: <code>{{ secret }}</code></p>
    <form @submit.prevent="verify">
      <input v-model="token" placeholder="Enter 6-digit code" maxlength="6" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Verifying...' : 'Enable 2FA' }}
      </button>
    </form>
    <button @click="skip" class="skip" :disabled="loading">Skip</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useDialog } from '../composables/useDialog'

const router = useRouter()
const { showSuccess, showError } = useDialog()

const qrCode = ref(null)
const secret = ref('')
const token = ref('')
const loading = ref(false)

onMounted(async () => {
  const userId = localStorage.getItem('userId')
  if (!userId) return router.push('/register')
  
  try {
    const res = await axios.post('http://localhost:5000/2fa/enable', null, {
      params: { user_id: userId }
    })
    qrCode.value = res.data.qr_code
    secret.value = res.data.secret
  } catch (err) {
    const msg = err.response?.data?.detail || err.message || 'Failed to generate QR'
    await showError(msg)
  }
})

const verify = async () => {
  loading.value = true
  try {
    const userId = localStorage.getItem('userId')
    const res = await axios.post('http://localhost:5000/2fa/verify', null, {
      params: { user_id: userId, code: token.value }
    })
    
    // Store JWT token
    localStorage.setItem('token', res.data.access_token)
    
    await showSuccess('2FA enabled successfully!')
    router.push('/dashboard')
  } catch (err) {
    const msg = err.response?.data?.detail || err.message || 'Invalid code'
    await showError(msg)
  } finally {
    loading.value = false
  }
}

const skip = () => {
  router.push('/')
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  text-align: center;
}
h1 { margin-bottom: 10px; color: #333; }
.subtitle { color: #666; margin-bottom: 20px; }
.qr { width: 200px; margin: 20px 0; border-radius: 10px; }
.secret { font-size: 12px; color: #666; margin-bottom: 20px; }
code {
  background: #f0f0f0;
  padding: 5px 10px;
  border-radius: 5px;
  color: #667eea;
  font-weight: 600;
}
input {
  width: 100%;
  padding: 15px;
  margin-bottom: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 18px;
  text-align: center;
  letter-spacing: 5px;
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
  margin-bottom: 10px;
  transition: transform 0.2s;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
button:not(:disabled):hover { transform: translateY(-2px); }
.skip {
  background: transparent;
  color: #666;
  border: 2px solid #ddd;
}
</style>
