<template>
  <v-dialog v-model="dialog" persistent>
    <v-card>
      <v-card-title>
        <span class="headline">Rename</span>
      </v-card-title>
      <v-form ref="form" @submit.prevent="confirm">
        <v-card-text>
          <v-text-field v-model="name" :rules="nameRules" label="New Name" autofocus clearable style="padding-left: 8px; padding-right: 8px"></v-text-field>
          <v-checkbox v-model="keepExt" hide-details density="comfortable" label="Keep Extension"></v-checkbox>
          <v-expand-transition>
            <v-alert v-if="success" color="success">Renamed!</v-alert>
          </v-expand-transition>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false" :disabled="loading">Cancel</v-btn>
          <v-btn type="submit" color="info" text :loading="loading">Rename</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="popup" timeout="2000" color="error">{{errMsg}}</v-snackbar>
</template>

<script>
import {getFileExtension, getFileStem, post} from "@/utils";
import {systemState} from "@/system";

export default {
  name: "RenameFileDialog",
  emits: ['confirm'],
  data() {
    return {
      dialog: false,
      loading: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 255 || 'Name must be less than 255 characters',
        v => '/*\\?:"<>|'.indexOf(v) === -1 || 'Name cannot contain the following characters: \\/:*?"<>|'
      ],
      keepExt: true,
      file: {},
      errMsg: '',
      popup: false,
      success: false
    }
  },
  methods: {
    show(file) {
      this.dialog = true
      this.success = false
      this.loading = false
      this.keepExt = true
      this.file = file
      this.name = getFileStem(file.name)
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
      post('/file/rename', {
        sessionId: systemState.currentSession,
        path: this.file.path,
        name: this.name + (this.keepExt ? getFileExtension(this.file.name) : '')
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
    },
  },
  watch: {
    keepExt(val){
      let ext = getFileExtension(this.file.name)
      if(val && this.name.endsWith(ext) && ext !== ''){
        this.name = this.name.slice(0, -ext.length)
      }else if(!val && !this.name.endsWith(ext)){
        this.name += ext
      }
    }
  }
}
</script>

<style scoped>

</style>
