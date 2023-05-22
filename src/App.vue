<template>
  <p>{{ `This is index.html, ${userName}` }}</p>
  <a href="login">Tap to login</a>
</template>

<script>
import {systemState} from "@/system";
import {requestLoginBySession} from "@/user-manager";

export default {
  name: "App",
  data() {
    return {
      userName: ""
    }
  },
  created() {
    let sessionId = systemState.currentSession;
    let m = this;
    requestLoginBySession(sessionId)
        .then(res => m.responseLogin(res));

  },
  methods: {
    responseLogin(response) {
      if (response.success) {
        this.userName = response.data;
      } else {
        window.alert(response.message);
      }
    }
  }
}
</script>

<style scoped>

</style>