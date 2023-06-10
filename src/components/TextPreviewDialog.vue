<template>
  <v-dialog v-model="dialog" persistent>
    <v-card :loading="loading">
      <template #loader>
        <v-progress-linear v-if="loading" color="primary" indeterminate></v-progress-linear>
      </template>
      <v-card-title>
        <span class="headline">Text Preview</span>
      </v-card-title>
      <v-card-text style="max-height: 60vh; overflow-y: auto; white-space: pre-wrap">
        {{text}}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
import {systemState} from "@/system";

export default {
  name: "TextPreviewDialog",
  props: ['src'],
  data(){
    return {
      dialog: false,
      loading: true,
      text: '',
      textCache: ''
    }
  },
  methods: {
    show(){
      this.dialog = true
      this.text = ''
      this.loading = false

      setTimeout(()=>{
        this.getText()
      }, 100)
    },
    getText(){
      if(!this.src) return
      this.loading = true

      axios.defaults.baseURL = systemState.globalSettings.backendUrl
      axios.get(this.src).then((res)=> {
        if(res.data instanceof Object){
          this.textCache = JSON.stringify(res.data)
        }else{
          this.textCache = res.data.toString()
        }
        this.text = this.textCache.substr(0, 1024)
        this.loading = false
      }).catch((err) => {
        window.alert(err)
        this.loading = false
      });
    },
    close(){

    }
  }
}
</script>

<style scoped>

</style>
