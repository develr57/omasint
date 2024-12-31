import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    http: true,
    host: true,
    hmr: false, //{ port: 80 },
    port: 8008,
    watch: {
      usePolling: true,
    },
  },
});
