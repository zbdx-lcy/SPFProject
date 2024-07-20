const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
    port: 8081,
    proxy: 'http://localhost:8000',
  },
  transpileDependencies: true,
  lintOnSave:false
})
