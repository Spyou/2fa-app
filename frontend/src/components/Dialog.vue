<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div v-if="isOpen" class="dialog-overlay" @click="close">
        <div class="dialog-box" @click.stop>
          <div class="dialog-header" :class="type">
            <span class="dialog-icon">{{ iconMap[type] }}</span>
            <h3>{{ title }}</h3>
          </div>
          <div class="dialog-body">
            <p>{{ message }}</p>
          </div>
          <div class="dialog-footer">
            <button @click="close" class="dialog-btn">OK</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Notice' },
  message: { type: String, required: true },
  type: { type: String, default: 'info' }
})

const emit = defineEmits(['close'])
const isOpen = ref(true)

const iconMap = {
  success: '✓',
  error: '✕',
  info: 'ℹ',
  warning: '⚠'
}

const close = () => {
  isOpen.value = false
  setTimeout(() => emit('close'), 300)
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.dialog-box {
  background: white;
  border-radius: 16px;
  min-width: 320px;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  overflow: hidden;
  animation: dialog-slide 0.3s ease-out;
}

.dialog-header {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #eee;
}

.dialog-header.success {
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
  color: white;
}

.dialog-header.error {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
}

.dialog-header.info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.dialog-header.warning {
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  color: white;
}

.dialog-icon {
  width: 32px;
  height: 32px;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.dialog-body {
  padding: 24px;
}

.dialog-body p {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.dialog-footer {
  padding: 16px 24px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #eee;
}

.dialog-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.dialog-btn:hover {
  transform: translateY(-2px);
}

.dialog-enter-active, .dialog-leave-active {
  transition: opacity 0.3s;
}

.dialog-enter-from, .dialog-leave-to {
  opacity: 0;
}

@keyframes dialog-slide {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
