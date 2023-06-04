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
        <v-list-item prepend-icon="mdi-view-dashboard" title="Profile" value="profile"></v-list-item>
        <v-list-item prepend-icon="mdi-history" title="History" value="history"></v-list-item>
        <v-list-item prepend-icon="mdi-bell-outline" title="Notification" value="notification"></v-list-item>
        <v-list-item prepend-icon="mdi-logout" title="Logout" value="logout"></v-list-item>
      </v-list>

      <v-sheet class="bottom">
        <v-divider></v-divider>
        <v-list>
          <v-list-item title="Dark Mode" class="align-center">
            <template #prepend>
              <v-icon size="28" style="margin-inline-end: 16px">mdi-weather-night</v-icon>
            </template>
            <template #append>
              <v-switch v-model="darkMode" class="list-switch"></v-switch>
            </template>
          </v-list-item>
        </v-list>
      </v-sheet>
    </v-navigation-drawer>
  </v-layout>
</template>

<script>
export default {
  name: "UserDrawer",
  props: ['userInfo'],
  data(){
    return {
      drawer: false,
      darkMode: false
    }
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
