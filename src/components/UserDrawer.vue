<template>
  <v-layout style="z-index: 10088;">
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list-item
        :title="userInfo.name"
        :subtitle="userInfo.group"
        height="70">
        <template #prepend>
          <v-avatar>
            <v-icon size="48">mdi-account-circle</v-icon>
          </v-avatar>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Profile" value="profile" @click="clickItem('profile')"></v-list-item>
        <v-list-item prepend-icon="mdi-history" title="History" value="history" @click="clickItem('history')"></v-list-item>
        <v-list-item prepend-icon="mdi-bell-outline" title="Notification" value="notification" @click="clickItem('notification')">
          <template #append>
            <v-badge v-if="unread > 0" :color="unreadColor" :content="unread" inline></v-badge>
          </template>
        </v-list-item>
        <v-list-item prepend-icon="mdi-logout" title="Logout" value="logout" @click="clickItem('logout')"></v-list-item>
      </v-list>

      <v-sheet class="bottom">
        <v-divider></v-divider>
        <v-list>
          <v-list-item title="Dark Mode" class="align-center">
            <template #prepend>
              <v-icon size="28" style="margin-inline-end: 16px">mdi-weather-night</v-icon>
            </template>
            <template #append>
              <v-switch v-model="darkMode" class="list-switch" @update:modelValue="toggleTheme"></v-switch>
            </template>
          </v-list-item>
        </v-list>
      </v-sheet>
    </v-navigation-drawer>
  </v-layout>

  <ProfileDialog ref="profile" />
  <HistoryDialog ref="history" />
  <NotificationDialog ref="notification" />
</template>

<script>
import ProfileDialog from "@/components/ProfileDialog";
import { useTheme } from 'vuetify'
import {syncToLocalStorage, systemState} from "@/system";
import HistoryDialog from "@/components/HistoryDialog";
import NotificationDialog from "@/components/NotificationDialog";

export default {
  name: "UserDrawer",
  components: {NotificationDialog, HistoryDialog, ProfileDialog},
  props: ['userInfo'],
  setup(){
    const theme = useTheme()

    return {
      theme,
      toggleTheme: () => {
        theme.global.name.value = theme.global.current.value.dark ? 'lightTheme' : 'darkTheme'
        localStorage.setItem('theme', theme.global.name.value)
      }
    }
  },
  data(){
    return {
      drawer: false,
      darkMode: false,
      unread: 0,
      unreadColor: 'info'
    }
  },
  computed: {
  },
  methods: {
    clickItem(item) {
      if (item === 'profile') {
        this.$refs.profile.dialog = true
      } else if (item === 'history') {
        this.$refs.history.dialog = true
      } else if(item === 'logout'){
        this.logout()
      }else if(item === 'notification'){
        this.$refs.notification.dialog = true
      }
    },
    logout(){
      systemState.currentSession = undefined
      syncToLocalStorage()
      window.location.href = '/login.html'
    },
    syncNotification(){
      //TODO: 同步通知阅读情况

      //TODO: 标注未读消息
      let cot = systemState.unread === undefined ? 0 : parseInt(systemState.unread)
      this.unread = cot
      this.unreadColor = systemState.unreadImportant ? 'important' : 'info';


      //TODO: 将未读通知数写到systemState里面
      systemState.unread = 11
      systemState.unreadImportant = false
      syncToLocalStorage()
    }
  },
  created() {
    const theme = useTheme()
    this.darkMode = theme.global.current.value.dark

    setInterval(this.syncNotification, 10000)
  }
}
</script>

<style scoped>
.bottom{
  position: absolute;
  bottom: 0;
  width: 100%;
}

.list-switch{
  display: flex;
  align-items: center;

}
</style>
