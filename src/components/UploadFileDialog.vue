<template>
  <v-dialog v-model="dialog" persistent min-width="300px" width="auto">
    <v-card>
      <v-card-title>Upload File</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="">
          <v-file-input @submit.prevent="" ref="file" show-size counter multiple label="File upload" :loading="loading"></v-file-input>
<!--          <v-text-field style="max-height: 0; opacity: 0; position: absolute; top: 0"></v-text-field>-->
        </v-form>
        <v-progress-linear color="primary" max="100" :model-value="progress" :indeterminate="verifying"></v-progress-linear>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" @click="abort">
          Cancel
        </v-btn>
        <v-btn color="info" @click="confirm" :disabled="loading">
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <ConfirmDialog ref="confirm"/>
  <v-snackbar v-model="popup" timeout="3000" color="error">{{errMsg}}</v-snackbar>
</template>

<script>
import axios from "axios";
import {systemState} from "@/system";
import {post} from "@/utils";
import ConfirmDialog from "@/components/ConfirmDialog";

export default {
  name: "UploadFileDialog",
  components: {ConfirmDialog},
  props: ['root'],
  emits: ['confirm'],
  data() {
    return {
      dialog: false,
      loading: false,
      verifying: false,
      progress: 0,
      uploadToken: null,

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
    popErr(msg) {
      this.errMsg = msg
      this.popup = true
    },
    confirm() {
      this.request()
    },
    updateProgress(num) {
      this.verifying = false
      this.progress = num
    },
    request() {
      this.loading = true
      this.verifying = true
      this.upload()
    },
    abort(){
      if(!this.loading){
        this.dialog = false
        return
      }
      this.$refs.confirm.show('Warning', 'Are you sure to abort the upload?', true, () => {
        if(this.uploadToken){
          this.uploadToken.cancel('User canceled the request')
        }
      })
    },
    upload(){
      let fileInput = this.$refs.file
      let formData = new FormData();
      if(fileInput.files.length === 0){
        this.popErr('Please select at least one file')
        this.loading = false
        this.verifying = false
        return
      }
      for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files', fileInput.files[i]);
      }
      formData.append('root', this.root)
      formData.append('sessionId', systemState.currentSession)

      this.uploadToken = axios.CancelToken.source()
      let updateMethod = this.updateProgress
      axios.defaults.baseURL = systemState.globalSettings.backendUrl
      axios.post('/file/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        cancelToken: this.uploadToken.token,
        onUploadProgress: function(progressEvent) {
          let percent = Math.round((progressEvent.loaded / progressEvent.total) * 100); // 计算上传进度
          updateMethod(percent)
        }
      }).then(res => {
        res = res.data
        if(res.success){
          this.success = true
          setTimeout(() => {
            this.dialog = false
            this.$emit('confirm')
          }, 1000)
        }else{
          this.popErr(res.message)
        }
      }).catch(err => {
        this.popErr(err.message)
      }).finally(() => {
        this.loading = false
        this.verifying = false
      })
    }
  }
}
</script>

<style scoped>

</style>
