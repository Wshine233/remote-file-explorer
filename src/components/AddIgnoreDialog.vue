<template>
  <v-dialog v-model="dialog" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        <span class="headline">Add Ignore</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="target" :rules="targetRules" label="Target" required
                        hint="Absolute Path in server's machine." :loading="loading" :disabled="loading"/>
        </v-form>
        <v-alert v-model="popup" type="error" dismissible elevation="2" class="mt-3">
          {{errMsg}}
        </v-alert>
        <v-alert v-model="success" type="success" dismissible elevation="2" class="mt-3">
          Ignore added successfully
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" @click="dialog = false" :disabled="loading">
          Cancel
        </v-btn>
        <v-btn color="blue darken-1" @click="confirm" :disabled="loading">
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {systemState} from "@/system";
import {post} from "@/utils";

export default {
  name: "AddIgnoreDialog",
  emits: ['confirm'],
  data(){
    return {
      dialog: false,
      loading: false,
      target: '',
      targetRules: [
        v => !!v || 'Target is required',
        v => v.length <= 255 || 'Target must be less than 255 characters',
        v => !/[*\\?"<>|]/.test(v) || 'Target cannot contain the following characters: \\*?"<>|'
      ],
      errMsg: '',
      popup: false,
      success: false
    }
  },
  methods:{
    show(){
      this.dialog = true
      this.success = false
      this.loading = false
      this.root = '/'
    },
    popErr(msg){
      this.errMsg = msg
      this.popup = true
    },
    validate(){
      for (const rule of this.targetRules) {
        if(rule(this.target) !== true){
          this.popup = true
          this.errMsg = rule(this.target)
          return false
        }
      }
      return true
    },
    confirm(){
      if(this.validate()){
        this.request()
      }
    },
    request(){
      this.loading = true
      let target = this.target
      console.log('target: ', this.target)
      post('/ignore/add', {
        sessionId: systemState.currentSession,
        target: target
      }).then(res => {
        this.success = true
        this.popup = false
        setTimeout(() => {
          this.$emit('confirm')
          this.loading = false
          this.dialog = false
        }, 1000)
      }).catch(err => {
        this.popErr(err.message)
        this.loading = false
      })
    }
  }
}
</script>

<style scoped>

</style>
