import { createApp } from "vue";
import GuidePage from "./index.vue"

// Plugins
import { registerPlugins } from '@/plugins'

let app = createApp(GuidePage)
registerPlugins(app)
app.mount("#panel")
