const { defineConfig } = require('@vue/cli-service')
const path = require('path');
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir : process.env.NODE_ENV === 'production' ? 'dist' : 'dist-dev',
  // publicPath : process.env.NODE_ENV === 'production' ? 'dist' : 'dist-dev',
  filenameHashing : false,
  runtimeCompiler : true,
  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
