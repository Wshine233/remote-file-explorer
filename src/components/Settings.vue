<template>
  <v-dialog v-model="backendDialog">
    <v-card title="Set Address">
      <v-card-text>
        <v-text-field v-model="backendUrlEdit" label="Backend URL" hint="Backend server's address (e.g. http://127.0.0.1:1080)" clearable></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn loading="true">
          Test
          <template #loader>
            <v-progress-circular width="3" size="25" indeterminate color="info"></v-progress-circular>
          </template>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn @click="saveUrlEdit">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    v-model="dialog"
    fullscreen
    :scrim="false"
    transition="dialog-bottom-transition">
    <v-window v-model="step" :touch="true" class="fill-height">
      <v-window-item value="settings" v-if="mode === 'settings' || wait" class="fill-height">
        <v-card class="fill-height">
          <v-toolbar
            dark
            color="primary"
          >
            <v-btn icon dark @click="close">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Settings</v-toolbar-title>
          </v-toolbar>

          <div style="height: calc(100% - 64px); overflow-y: auto">
            <v-list lines="two" subheader>
              <v-list-subheader>Local</v-list-subheader>
              <v-list-item value="backend-url" @click="showUrlEdit">
                <template #title>
                  <v-list-item-title>Backend URL</v-list-item-title>
                  <v-list-item-subtitle>{{ backendUrl }}</v-list-item-subtitle>
                </template>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list
              lines="two"
              subheader
            >
              <v-list-subheader>User</v-list-subheader>
              <v-list-item title="Reset Password" subtitle="Reset your password. You need to enter your original password."
                           value="password" @click="showPasswordReset"></v-list-item>
              <v-list-item title="User Group" subtitle="admin"
                           value="group" @click="showGroup"></v-list-item>
            </v-list>

            <v-divider></v-divider>

            <v-list lines="two">
              <v-list-subheader>Super User</v-list-subheader>
              <v-list-item title="Manage Mounts" subtitle="Add, delete, edit mounts in current mount list." value="mount" @click="showWindow('mount')"></v-list-item>
              <v-list-item title="Manage Users" subtitle="Edit user permissions, or remove users." value="user" @click="showWindow('user')"></v-list-item>
              <v-list-item title="Manage Permissions" subtitle="Edit default permissions, or configure file rules." value="perm" @click="showWindow('perm')"></v-list-item>
              <v-list-item title="Broadcast Message" subtitle="Broadcast Message to all users." value="broadcast" @click="showMessage"></v-list-item>
            </v-list>
          </div>

        </v-card>
      </v-window-item>

      <MountWindow v-if="mode === 'mount' || wait" @back="showWindow('settings')"/>

      <UserWindow v-if="mode === 'user' || wait" @back="showWindow('settings')"/>

      <PermWindow v-if="mode === 'perm' || wait" @back="showWindow('settings')"/>

      <v-window-item v-if="mode === 'xxx' || wait"></v-window-item>
    </v-window>
  </v-dialog>

  <BroadcastDialog ref="message" :send-to="[]" />
  <PasswordResetDialog ref="password" />
  <GroupUpgradeRequestDialog ref="group" />
</template>


<script>
import {systemState} from "@/system";
import MountWindow from "@/components/MountWindow";
import UserWindow from "@/components/UserWindow";
import PermWindow from "@/components/PermWindow";
import BroadcastDialog from "@/components/BroadcastDialog";
import PasswordResetDialog from "@/components/PasswordResetDialog";
import GroupUpgradeRequestDialog from "@/components/GroupUpgradeRequestDialog";

export default {
  name: "Settings",
  components: {GroupUpgradeRequestDialog, PasswordResetDialog, BroadcastDialog, PermWindow, UserWindow, MountWindow},
  data() {
    return {
      dialog: false,
      backendDialog: false,
      backendUrl: "",
      backendUrlEdit: "",
      step: "settings",
      mode: "settings",
      wait: false
    }
  },
  computed: {

  },
  methods:{
    showUrlEdit(){
      this.backendDialog = true
      this.backendUrlEdit = this.backendUrl
    },
    saveUrlEdit(){
      this.backendUrl = this.backendUrlEdit
      this.backendDialog = false
    },
    close(){
      this.step = "settings"
      this.dialog = false
    },
    showWindow(step){
      if(this.wait) return

      this.wait = true
      this.mode = step
      setTimeout(() => {
        this.step = step
      }, 150)
      setTimeout(() => {
        if(this.step !== step){
          this.mode = this.step
        }
        this.wait = false
      }, 450)
    },
    showMessage(){
      this.$refs.message.dialog = true
    },
    showPasswordReset(){
      this.$refs.password.dialog = true
    },
    showGroup(){
      this.$refs.group.dialog = true
    }
  },
  watch: {
    dialog(val){
      if(val){
        this.backendUrl = systemState.globalSettings.backendUrl
      }
    }
  }
}
</script>

<style scoped>
.list-switch{
  display: flex;
}
</style>
