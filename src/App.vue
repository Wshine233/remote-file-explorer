<template>
  <p>{{ `This is index.html, ${userName}` }}</p>
  <a href="login" v-if="!loggedIn">Tap to login</a>
  <a style="display: block; cursor: pointer" v-if="loggedIn" @click="logout">Logout</a>
</template>

<script>
import {systemState, syncToLocalStorage as syncState} from "@/system";
import {requestLoginBySession, requestGetUserInfo, requestLogout} from "@/user-manager";

export default {
  name: "App",
  data() {
    return {
      userName: "",
      loggedIn: false
    }
  },
  created() {
    let sessionId = systemState.currentSession;
    let m = this;

    if(sessionId === undefined) return

    requestLoginBySession(sessionId)
        .then(res => m.responseLogin(res));

  },
  methods: {
    responseLogin(response) {
      if (response.success) {
        this.showUsername()
        this.loggedIn = true;
      } else {
        systemState.currentSession = undefined;
        syncState();
        window.alert(response.message);

      }
    },
    showUsername(){
      requestGetUserInfo(systemState.currentSession, ['name'])
          .then(res => {
            if(res.success){
              this.userName = res.data['name'];
            }else{
              window.alert(res.message);
            }
          })
    },
    logout(){
      requestLogout(systemState.currentSession)
          .then(res => {
            if(res.success){
              window.location.href = "/";
            }else{
              window.alert(res.message);
            }
          })
    }
  }
}
</script>

<style scoped>

</style>