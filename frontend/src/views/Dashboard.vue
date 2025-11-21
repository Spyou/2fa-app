<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="logo-section">
        <div class="logo">
          <div class="logo-icon">🔐</div>
          <h2>SecureApp</h2>
        </div>
      </div>

      <div class="menu-section">
        <p class="menu-title">MENU</p>
        <nav class="nav-menu">
          <a href="#" class="nav-item active">
            <span class="icon">📊</span>
            <span>Dashboard</span>
          </a>
          <a href="#" class="nav-item">
            <span class="icon">🔒</span>
            <span>Security</span>
          </a>
          <a href="#" class="nav-item">
            <span class="icon">👤</span>
            <span>Profile</span>
          </a>
          <a href="#" class="nav-item">
            <span class="icon">⚙️</span>
            <span>Settings</span>
          </a>
        </nav>
      </div>

      <div class="menu-section">
        <p class="menu-title">GENERAL</p>
        <nav class="nav-menu">
          <a href="#" class="nav-item">
            <span class="icon">❓</span>
            <span>Help</span>
          </a>
          <a href="#" class="nav-item" @click.prevent="logout">
            <span class="icon">🚪</span>
            <span>Logout</span>
          </a>
        </nav>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Bar -->
      <header class="top-bar">
        <div class="search-bar">
          <span class="search-icon">🔍</span>
          <input type="text" placeholder="Search" />
          <span class="shortcut">⌘F</span>
        </div>
        <div class="top-actions">
          <button class="icon-btn">🔔</button>
          <div class="user-profile">
            <img :src="'https://ui-avatars.com/api/?name=' + username + '&background=10b981&color=fff'" :alt="username" />
            <div class="user-info">
              <p class="user-name">{{ username }}</p>
              <p class="user-email">{{ username }}@mail.com</p>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Header -->
      <div class="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>Manage your account security and settings</p>
        </div>
        <div class="header-actions">
          <button class="btn-primary" @click="router.push('/setup-2fa')">+ Setup 2FA</button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card green">
          <div class="stat-header">
            <h3>2FA Status</h3>
            <button class="stat-arrow">↗</button>
          </div>
          <div class="stat-value">Enabled</div>
          <div class="stat-footer">
            <span class="trend-badge">✓ Protected</span>
          </div>
        </div>

        <div class="stat-card white">
          <div class="stat-header">
            <h3>Active Sessions</h3>
            <button class="stat-arrow">↗</button>
          </div>
          <div class="stat-value">1</div>
          <div class="stat-footer">
            <span class="trend-badge">Current device</span>
          </div>
        </div>

        <div class="stat-card white">
          <div class="stat-header">
            <h3>Security Score</h3>
            <button class="stat-arrow">↗</button>
          </div>
          <div class="stat-value">95/100</div>
          <div class="stat-footer">
            <span class="trend-badge">Excellent</span>
          </div>
        </div>

        <div class="stat-card white">
          <div class="stat-header">
            <h3>Account Status</h3>
            <button class="stat-arrow">↗</button>
          </div>
          <div class="stat-value">Active</div>
          <div class="stat-footer">
            <span class="status-active">✓ Verified</span>
          </div>
        </div>
      </div>

      <!-- Content Grid -->
      <div class="content-grid">
        <!-- Security Features -->
        <div class="card large">
          <h3 class="card-title">Security Features</h3>
          <div class="features-list">
            <div class="feature-item">
              <div class="feature-icon success">✓</div>
              <div class="feature-details">
                <h4>Two-Factor Authentication</h4>
                <p>TOTP-based 2FA protection</p>
              </div>
              <span class="status-badge active">Active</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon success">✓</div>
              <div class="feature-details">
                <h4>JWT Token Authentication</h4>
                <p>Secure session management</p>
              </div>
              <span class="status-badge active">Active</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon success">✓</div>
              <div class="feature-details">
                <h4>Password Encryption</h4>
                <p>bcrypt hashing protection</p>
              </div>
              <span class="status-badge active">Active</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon success">✓</div>
              <div class="feature-details">
                <h4>Database Security</h4>
                <p>PostgreSQL + SQLAlchemy</p>
              </div>
              <span class="status-badge active">Active</span>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="card">
          <h3 class="card-title">Recent Activity</h3>
          <div class="activity-list">
            <div class="activity-item">
              <span class="activity-icon green">🔑</span>
              <div class="activity-details">
                <h4>Login Success</h4>
                <p>{{ currentTime }}</p>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-icon blue">🔐</span>
              <div class="activity-details">
                <h4>2FA Enabled</h4>
                <p>Today</p>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-icon purple">👤</span>
              <div class="activity-details">
                <h4>Account Created</h4>
                <p>Today</p>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-icon orange">⚙️</span>
              <div class="activity-details">
                <h4>Profile Updated</h4>
                <p>Today</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDialog } from '../composables/useDialog'

const router = useRouter()
const { showSuccess } = useDialog()

const username = ref('')
const currentTime = ref('')

onMounted(() => {
  username.value = localStorage.getItem('username') || 'User'
  
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/')
  }

  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true
  })
})

const logout = async () => {
  localStorage.clear()
  await showSuccess('Logged out successfully!')
  router.push('/')
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard {
  display: flex;
  min-height: 100vh;
  background: #f5f7f9;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: white;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
}

.logo-section {
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.logo h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
}

.menu-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu-title {
  font-size: 11px;
  font-weight: 600;
  color: #9ca3af;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: #6b7280;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
}

.nav-item .icon {
  font-size: 18px;
}

.nav-item:hover {
  background: #f9fafb;
  color: #1a1a1a;
}

.nav-item.active {
  background: #10b981;
  color: white;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: #059669;
  border-radius: 0 4px 4px 0;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 32px;
}

/* Top Bar */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  gap: 24px;
}

.search-bar {
  flex: 1;
  max-width: 480px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 12px 20px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.search-icon {
  font-size: 18px;
  color: #9ca3af;
}

.search-bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1a1a1a;
}

.search-bar input::placeholder {
  color: #9ca3af;
}

.shortcut {
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 6px;
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icon-btn {
  width: 44px;
  height: 44px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  border-color: #10b981;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.user-profile img {
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.user-info {
  padding-right: 12px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.user-email {
  font-size: 12px;
  color: #9ca3af;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  gap: 24px;
}

.page-header h1 {
  font-size: 36px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.page-header p {
  font-size: 15px;
  color: #6b7280;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary {
  padding: 12px 24px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #059669;
  transform: translateY(-1px);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.stat-card.green {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.stat-header h3 {
  font-size: 14px;
  font-weight: 500;
  opacity: 0.9;
}

.stat-arrow {
  width: 32px;
  height: 32px;
  background: rgba(255,255,255,0.2);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
}

.stat-card.white .stat-arrow {
  background: #f3f4f6;
}

.stat-value {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 12px;
}

.stat-card.white .stat-value {
  color: #1a1a1a;
}

.trend-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  padding: 6px 10px;
  background: rgba(255,255,255,0.2);
  border-radius: 8px;
}

.stat-card.white .trend-badge {
  background: #f0fdf4;
  color: #059669;
}

.status-active {
  display: inline-block;
  font-size: 12px;
  padding: 6px 10px;
  background: #d1fae5;
  color: #059669;
  border-radius: 8px;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

/* Features List */
.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
}

.feature-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.feature-icon.success {
  background: #d1fae5;
  color: #059669;
}

.feature-details {
  flex: 1;
}

.feature-details h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.feature-details p {
  font-size: 13px;
  color: #6b7280;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: #d1fae5;
  color: #059669;
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 10px;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.activity-icon.green { background: #d1fae5; }
.activity-icon.blue { background: #dbeafe; }
.activity-icon.purple { background: #e9d5ff; }
.activity-icon.orange { background: #fed7aa; }

.activity-details h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.activity-details p {
  font-size: 12px;
  color: #9ca3af;
}

/* Responsive */
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .main-content {
    margin-left: 0;
  }
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .top-bar {
    flex-direction: column;
  }
  .search-bar {
    max-width: 100%;
  }
}
</style>
