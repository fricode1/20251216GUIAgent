import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3002,
    proxy: {
      '/violation': {
        target: 'http://62.168.243.13:8000',
        changeOrigin: true
      }
    }
  }
})
