import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: './',
  base: '/static/',
  build: {
    outDir: '../jobs/static/dist',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/main.js'),
      },
      output: {
        entryFileNames: 'js/[name].js',
        chunkFileNames: 'js/[name].js',
        assetFileNames: 'css/[name].[ext]',
      },
    },
  },
  server: {
    port: 5173,
    cors: true,
  },
})
