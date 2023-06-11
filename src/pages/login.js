import {createApp} from "vue";
import LoginPage from "./login.vue";

console.log("login.js")
let app = createApp(LoginPage)
app.mount("#panel");
