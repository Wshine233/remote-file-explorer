import { createApp } from "vue";
import IndexPage from "./App.vue"
import {Button} from "vant";
import "vant/lib/index.css";

import 'vuetify/styles'
import {createVuetify} from 'vuetify';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(IndexPage)
app.use(Button).use(vuetify)
app.mount("#app")
