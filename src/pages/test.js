import { createApp } from "vue";
import IndexPage from "./test.vue"
import Vue3VideoPlayer from '@cloudgeek/vue3-video-player'
import '@cloudgeek/vue3-video-player/dist/vue3-video-player.css'


// Plugins
import { registerPlugins } from '@/plugins'

let app = createApp(IndexPage)
app = app.use(Vue3VideoPlayer, {
  lang: 'zh-CN'
})
registerPlugins(app)
app.mount("#app")
