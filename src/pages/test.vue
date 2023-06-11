<template>
  <div style="width: 100%; height: 100%">
    <!--  <p>{{ `This is index.html, ${userName}` }}</p>-->
    <!--  <a href="login" v-if="!loggedIn">Tap to login</a>-->
    <!--  <a style="display: block; cursor: pointer" v-if="loggedIn" @click="logout">Logout</a>-->
    <div id="file-list">
      <FileList ref="list"/>
      <!--    <Settings/>-->
    </div>
  </div>
</template>

<script>
import {systemState, syncToLocalStorage as syncState} from "@/system";
import {requestLoginBySession, requestGetUserInfo, requestLogout} from "@/user-manager";
import FileList from "@/components/FileList";
import Settings from "@/components/Settings";

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

    if (sessionId === undefined) {
      window.location.href = "/login.html";
      return;
    }

    requestLoginBySession(sessionId)
      .then(res => m.responseLogin(res));

  },

  //引入文件列表查看组件
  components: {
    Settings,
    FileList
  },

  methods: {
    responseLogin(response) {
      if (response.success) {
        // this.showUsername()
        this.$refs.list.changePath(this.parsePath())
        this.loggedIn = true;
      } else {
        systemState.currentSession = undefined;
        syncState();
        window.alert(response.message);
        window.location.href = "/login.html";
      }
    },
    parsePath() {
      //get path from location.href
      let path = window.location.href.split('?')[1];
      path = decodeURI(path)
      if (path === undefined) {
        return '/'
      }
      path = path.split('&')
      for (let i = 0; i < path.length; i++) {
        if (path[i].startsWith('path=')) {
          return path[i].substr(5)
        }
      }
      return '/'
    },
    showUsername() {
      requestGetUserInfo(systemState.currentSession, ['name'])
        .then(res => {
          if (res.success) {
            this.userName = res.data['name'];
          } else {
            window.alert(res.message);
          }
        })
    },
    logout() {
      requestLogout(systemState.currentSession)
        .then(res => {
          if (res.success) {
            window.location.href = "/";
          } else {
            window.alert(res.message);
          }
        })
    }
  }
}
</script>

<style scoped>
#file-list {
  width: 100%;
  height: auto;
  box-sizing: border-box;
}

.btn {
  background-color: #1890ff;
}
</style>
