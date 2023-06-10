<template>
<v-dialog v-model="dialog">
  <v-card>
    <v-card-title>{{title}}</v-card-title>
    <v-card-text>{{content}}</v-card-text>
    <v-card-actions v-if="warn">
      <v-spacer></v-spacer>
      <v-btn color="info" @click="confirm(true)">
        Yes
      </v-btn>
      <v-btn color="error" @click="confirm(false)">
        No
      </v-btn>
    </v-card-actions>
    <v-card-actions v-else>
      <v-spacer></v-spacer>
      <v-btn color="error" @click="confirm(false)">
        No
      </v-btn>
      <v-btn color="info" @click="confirm(true)">
        Yes
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
</template>

<script>
export default {
  name: "ConfirmDialog",
  data(){
    return {
      dialog: false,
      title: "",
      content: "",
      warn: true,  //如果是警告类窗口，则对调选项以防止误操作
      callback: null
    }
  },
  methods:{
    show(title, content, warn = true, callback = null){
      this.title = title
      this.content = content
      this.warn = warn
      this.dialog = true
      this.callback = callback
    },
    confirm(result){
      if(this.callback !== null)
        this.callback(result)
      this.dialog = false
    }
  }
}
</script>

<style scoped>

</style>
