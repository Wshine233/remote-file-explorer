const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    pages: {
        index:{
            entry: "./src/main.js",  //入口js文件
            template: "./src/index.html",  //主页面
            filename: "index.html",  //打包后的html文件名称
            title: "Remote File Explorer"  //打包后的.html中<title>标签的文本内容
        },
        login: {
            entry: "./src/module/login.js",
            template: "./src/module/login.html",
            filename: "login.html",
            title: "RFE - Login"
        }
    }
})
