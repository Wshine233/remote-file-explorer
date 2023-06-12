<template>
  <v-dialog v-model="dialog" persistent max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">Create Folder</span>
      </v-card-title>
      <v-form ref="form" @submit.prevent="confirm">
        <v-card-text>
          <v-text-field v-model="name" :rules="nameRules" label="Folder Name" autofocus clearable  style="padding-left: 8px; padding-right: 8px"></v-text-field>
          <v-expand-transition>
            <v-alert v-if="success" color="success">Folder Created!</v-alert>
          </v-expand-transition>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false" :disabled="loading">Cancel</v-btn>
          <v-btn type="submit" color="info" text :loading="loading">Create</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="popup" timeout="2000" color="error">{{errMsg}}</v-snackbar>
</template>

<script>
import {post} from "@/utils";
import {systemState} from "@/system";

export default {
  name: "CreateFolderDialog",
  props: ['path'],
  emits: ['confirm'],
  data() {
    return {
      dialog: false,
      loading: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 255 || 'Name must be less than 255 characters',
        v => !/[/*\\?:"<>|]/.test(v) || 'Name cannot contain the following characters: \\/:*?"<>|'
      ],
      errMsg: '',
      popup: false,
      success: false
    }
  },
  methods: {
    show() {
      this.dialog = true
      this.success = false
      this.loading = false
    },
    popErr(msg){
      this.errMsg = msg
      this.popup = true
    },
    validate(){
      for (const rule of this.nameRules) {
        if(rule(this.name) !== true){
          this.popup = true
          this.errMsg = rule(this.name)
          return false
        }
      }
      return true
    },
    confirm() {
      if (this.validate()) {
        this.request()
      }
    },
    request(){
      this.loading = true
      post('/file/create-folder', {
        sessionId: systemState.currentSession,
        path: this.path,
        name: this.name
      }).then(res => {
        this.success = true
        setTimeout(() => {
          this.$emit('confirm', this.name)
          this.dialog = false
        }, 1500)
      }).catch(err =>{
        this.loading = false
        this.popErr(err.message)
      })
    }
  }
}
</script>

<style scoped>

</style>
