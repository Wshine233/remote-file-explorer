import { createApp } from "vue";
import IndexPage from "./test.vue"

// Plugins
import { registerPlugins } from '@/plugins'

const app = createApp(IndexPage)
registerPlugins(app)
app.mount("#app")
