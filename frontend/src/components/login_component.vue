<template>
  <div>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Login</button>
    
    <div v-if="requires2FA">
      <input v-model="token" placeholder="2FA Code" />
      <button @click="verify2FA">Verify</button>
    </div>
    
    <div v-if="qrCode">
      <img :src="qrCode" alt="QR Code" />
      <p>Secret: {{ secret }}</p>
      <button @click="enable2FA">Enable 2FA</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      token: '',
      userId: null,
      requires2FA: false,
      qrCode: null,
      secret: null
    }
  },
  methods: {
    async login() {
      const res = await axios.post('http://localhost:5000/login', {
        username: this.username,
        password: this.password
      });
      this.userId = res.data.user_id;
      this.requires2FA = res.data.requires_2fa;
      
      if (!this.requires2FA) {
        const qr = await axios.post('http://localhost:5000/2fa/enable', {
          user_id: this.userId
        });
        this.qrCode = qr.data.qr_code;
        this.secret = qr.data.secret;
      }
    },
    async verify2FA() {
      await axios.post('http://localhost:5000/2fa/verify', {
        user_id: this.userId,
        token: this.token
      });
      alert('Login successful!');
    },
    async enable2FA() {
      await axios.post('http://localhost:5000/2fa/verify', {
        user_id: this.userId,
        token: this.token
      });
      alert('2FA enabled!');
    }
  }
}
</script>
