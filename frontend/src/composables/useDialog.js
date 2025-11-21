import { h, render } from 'vue'
import Dialog from '../components/Dialog.vue'

export function useDialog() {
  const showDialog = (options) => {
    return new Promise((resolve) => {
      const container = document.createElement('div')
      document.body.appendChild(container)

      const close = () => {
        render(null, container)
        document.body.removeChild(container)
        resolve()
      }

      const vnode = h(Dialog, {
        ...options,
        onClose: close
      })

      render(vnode, container)
    })
  }

  const showSuccess = (message, title = 'Success') => {
    return showDialog({ message, title, type: 'success' })
  }

  const showError = (message, title = 'Error') => {
    return showDialog({ message, title, type: 'error' })
  }

  const showInfo = (message, title = 'Info') => {
    return showDialog({ message, title, type: 'info' })
  }

  return {
    showDialog,
    showSuccess,
    showError,
    showInfo
  }
}
