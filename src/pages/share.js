import { createApp } from "vue";
import SharePage from "./share.vue"

// Plugins
import { registerPlugins } from '@/plugins'

const app = createApp(SharePage)
registerPlugins(app)
app.mount("#app")
