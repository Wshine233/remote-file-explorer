<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title style="padding-bottom: 2px">Reset Password</v-card-title>

      <v-card-text>
        <v-text-field v-model="passwordOld" label="Old Password" type="password" :rules="passwordOldRules" required :loading="loading" :disabled="loading"></v-text-field>
        <v-text-field v-model="password" label="Password" type="password" :rules="passwordRules" required :loading="loading" :disabled="loading"></v-text-field>
        <v-text-field v-model="passwordConfirm" label="Confirm Password" type="password" :rules="passwordConfirmRules" required :loading="loading" :disabled="loading"></v-text-field>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="reset" :disabled="loading" :loading="loading">Reset</v-btn>
      </v-card-actions>

    </v-card>
  </v-dialog>

  <v-snackbar v-model="popup" :color="success ? 'success' : 'error'" timeout="3000">{{errMsg}}</v-snackbar>
</template>

<script>
import {updatePassword} from "@/utils";

export default {
  name: "PasswordResetDialog",
  data(){
    return {
      dialog: false,
      loading: false,
      passwordOld: "",
      password: "",
      passwordConfirm: "",
      passwordOldRules: [
        v => !!v || 'Password is required',
        v => v.length >= 6 || 'Password must be at least 8 characters',
        v => v.length <= 16 || 'Password must be at most 16 characters',
      ],
      passwordRules: [
        v => !!v || 'Password is required',
        v => v.length >= 6 || 'Password must be at least 8 characters',
        v => v.length <= 16 || 'Password must be at most 16 characters',
      ],
      passwordConfirmRules: [
        v => !!v || 'Password is required',
        v => v === this.password || 'Password does not match',
      ],

      errMsg: "",
      popup: false,
      success: false,
    }
  },
  methods: {
    show(){
      this.dialog = true
      this.loading = false
      this.passwordOld = ""
      this.password = ""
      this.passwordConfirm = ""
    },
    reset() {
      this.confirm()
    },
    popErr(msg, success = false){
      this.errMsg = msg
      this.popup = true
      this.success = success
    },
    confirm(){
      if(!this.validate()){
        return
      }

      this.loading = true
      updatePassword(this.passwordOld, this.password).then(res => {
        this.loading = false
        this.dialog = false
        this.popErr("Password updated", true)
      }).catch(err => {
        this.loading = false
        this.popErr(err.message)
      })

    },
    validate(){
      for(let rule of this.passwordOldRules){
        if(rule(this.passwordOld) !== true){
          this.popErr(rule(this.passwordOld))
          return false
        }
      }

      for(let rule of this.passwordRules){
        if(rule(this.password) !== true){
          this.popErr(rule(this.password))
          return false
        }
      }

      for(let rule of this.passwordConfirmRules){
        if(rule(this.passwordConfirm) !== true){
          this.popErr(rule(this.passwordConfirm))
          return false
        }
      }

      return true
    }
  }
}
</script>

<style scoped>

</style>
