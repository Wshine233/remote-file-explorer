<template>
  <v-dialog v-model="dialog" max-width="500px" :persistent="loading">
    <v-card>
      <v-card-title>Set Perm Group</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field v-model="name" :rules="nameRules" label="Name" required :readonly="!modeAdd" :loading="loading" :disabled="loading"></v-text-field>
          <v-text-field v-model="perm" label="Permission" required :loading="loading" :disabled="loading" hint="'adxms', '-' means no permission ('ad-ms')"></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn v-if="!modeAdd" color="error" @click="remove" :disabled="loading">
          Remove
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="info" @click="confirm" :disabled="loading">
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <ConfirmDialog ref="confirm" />
  <v-snackbar v-model="popup" timeout="2000" color="error">{{errMsg}}</v-snackbar>
</template>

<script>
import {post} from "@/utils";
import {systemState} from "@/system";
import ConfirmDialog from "@/components/ConfirmDialog";

export default {
  name: "SetPermDialog",
  components: {ConfirmDialog},
  emits: ['confirm'],
  data(){
    return {
      dialog: false,
      loading: false,
      modeAdd: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 255 || 'Name must be less than 255 characters',
        v => this.validateName(v) || 'Name can only contain letters, numbers, underscores, and hyphens'
      ],
      perm: '',
      errMsg: '',
      popup: false,
    }
  },
  methods:{
    popMsg(msg){
      this.errMsg = msg
      this.popup = true
    },
    show(add, name = '', perm = ''){
      this.dialog = true
      this.loading = false
      this.modeAdd = add
      this.name = name
      this.perm = perm
    },
    validateName(name){
      //只允许包含字母、数字、下划线、中划线
      return /^[a-zA-Z0-9_\-]+$/.test(name)
    },
    validate(){
      for (const rule of this.nameRules) {
        if(rule(this.name) !== true){
          return false
        }
      }
      return true
    },
    remove(){
      this.$refs.confirm.show('Warning', 'Are you sure to remove this perm group?\nAll users in this group will be moved to default group!', true, res => {
        if(!res) return
        this.loading = true
        post('/perm/remove', {
          sessionId: systemState.currentSession,
          id: this.name,
        }).then(res => {
          this.loading = false
          this.$emit('confirm')
          this.dialog = false
        }).catch(err => {
          this.loading = false
          this.popMsg(err.message)
        })
      })
    },
    confirm(){
      if(!this.validate()) return
      if(this.modeAdd){
        this.loading = true
        post('/perm/add', {
          sessionId: systemState.currentSession,
          id: this.name,
          perm: this.perm
        }).then(res => {
          this.loading = false
          this.$emit('confirm')
          this.dialog = false
        }).catch(err => {
          this.loading = false
          this.popMsg(err.message)
        })
      }else{
        this.loading = true
        post('/perm/update', {
          sessionId: systemState.currentSession,
          id: this.name,
          perm: this.perm
        }).then(res => {
          this.loading = false
          this.$emit('confirm')
          this.dialog = false
        }).catch(err => {
          this.loading = false
          this.popMsg(err.message)
        })
      }
    }
  }
}
</script>

<style scoped>

</style>
