<template>
  <v-sheet class="flex-panel" elevation="3">
    <v-img src="@/assets/logo.png" style="max-width: 480px; padding: 20px"></v-img>
    <v-text-field v-model="backend" label="Backend Server Address">
      <template #append-inner>
        <v-btn icon variant="flat" color="primary" @click="check" density="comfortable" :loading="loading" :disabled="success">
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
      </template>
    </v-text-field>

    <v-slide-y-transition>
      <v-alert v-model="alertPop" :type="success ? 'success' : 'error'">
        <template #text>
          {{alertContent}}
        </template>
      </v-alert>
    </v-slide-y-transition>


  </v-sheet>
</template>

<script>
import {syncToLocalStorage, systemState} from "@/system";
import axios from "axios";

export default {
  name: "GuidePage",
  data(){
    return {
      loading: false,
      backend: '',

      alertPop: false,
      alertContent: '',
      success: false
    }
  },
  methods:{
    next(){
      window.location.href = 'test.html'
    },
    popMsg(msg){
      this.alertPop = false
      this.alertContent = msg

      setTimeout(()=>{
        this.alertPop = true
      }, 150)
    },
    check(){
      if(this.backend === ''){
        this.popMsg('Please enter the backend server address.')
        return
      }

      this.loading = true
      axios.defaults.baseURL = this.backend
      axios.get('/test/hello').then(res=>{
        systemState.globalSettings.backendUrl = this.backend
        syncToLocalStorage()
        this.loading = false
        this.success = true
        this.popMsg('Successful! Redirecting..')
        setTimeout(()=>{
          this.next()
        }, 1500)
      }).catch(err => {
        this.popMsg('Backend server cannot be reached.')
        this.loading = false
      })
    },
    init(){
      this.backend = systemState.globalSettings.backendUrl
    }
  },
  mounted() {
    this.init()
  }
}
</script>

<style scoped>
.flex-panel{
  /*display: flex;*/
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
  max-width: 500px;

  padding: 20px;
}
</style>
