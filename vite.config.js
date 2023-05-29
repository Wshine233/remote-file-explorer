// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, {transformAssetUrls} from 'vite-plugin-vuetify'

// Utilities
import {defineConfig} from 'vite'
import {fileURLToPath, URL} from 'node:url'
import {createHtmlPlugin} from "vite-plugin-html";

const { resolve } = require('path')

// https://vitejs.dev/config/
export default defineConfig({
  root: './src/pages',
  build: {
    rollupOptions: {
      input: {
        index: resolve('src/pages/hello.html'),
        login: resolve('src/pages/login.html'), //key随意的，不影响
        register: resolve('src/pages/register.html'),  //key随意的，不影响
      }
    }
  },
  plugins: [
    vue({
      template: {transformAssetUrls}
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
    createHtmlPlugin({
      minify: true,
      pages: [
        {
          entry: './hello.js', //根据root的设置，
          template: 'src/pages/hello.html',
          filename: 'hello.html', //名字随意，但必须有
        },
        {
          entry: './test.js', //根据root的设置，
          template: 'src/pages/test.html',
          filename: 'test.html', //名字随意，但必须有
        },
        {
          entry: './login.js', //根据root的设置，
          template: 'src/pages/login.html',
          filename: 'login.html' //名字随意，但必须有
        },
        {
          entry: './register.js', //根据root的设置，
          template: 'src/pages/register.html',
          filename: 'register.html' //名字随意，但必须有
        }
      ]
    })
  ],
  define: {'process.env': {}},
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 3000,
  },
})
