<template>
  <v-dialog v-model="backendDialog">
    <v-card title="Set Value">
      <v-card-text>
        <v-text-field v-model="backendUrlEdit" label="Backend URL" hint="Backend server's address (e.g. http://127.0.0.1:1080)" clearable></v-text-field>
      </v-card-text>
      <v-card-actions>
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

    <v-card>
      <v-toolbar
        dark
        color="primary"
      >
        <v-btn
          icon
          dark
          @click="dialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Settings</v-toolbar-title>
      </v-toolbar>
      <v-list
        lines="two" subheader>
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
        <v-list-subheader>General</v-list-subheader>
        <v-list-item title="Notifications" subtitle="Notify me about updates to apps or games that I downloaded">
          <template v-slot:prepend>
            <v-checkbox v-model="notifications" class="list-switch"></v-checkbox>
          </template>
        </v-list-item>
        <v-list-item title="Sound" subtitle="Auto-update apps at any time. Data charges may apply">
          <template v-slot:prepend>
            <v-checkbox v-model="sound" class="list-switch"></v-checkbox>
          </template>
        </v-list-item>
        <v-list-item title="Auto-add widgets" subtitle="Automatically add home screen widgets">
          <template v-slot:prepend>
            <v-checkbox v-model="widgets" class="list-switch"></v-checkbox>
          </template>
        </v-list-item>
      </v-list>
    </v-card>
  </v-dialog>
</template>


<script>
import {systemState} from "@/system";

export default {
  name: "Settings",
  data() {
    return {
      dialog: false,
      backendDialog: false,
      backendUrl: "",
      backendUrlEdit: "",
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
