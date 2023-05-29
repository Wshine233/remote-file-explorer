import { createApp } from "vue";
import IndexPage from "./App.vue"
import {Button} from "vant";
import "vant/lib/index.css";

const app = createApp(IndexPage)
app.use(Button).mount("#app")
