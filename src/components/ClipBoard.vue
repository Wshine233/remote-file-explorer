<template>
  <v-slide-y-reverse-transition>
    <v-btn v-if="visible && show" class="float-btn" icon color="success" size="large" @click="toggleDrawer">
      <v-icon>mdi-clipboard-multiple-outline</v-icon>
    </v-btn>
  </v-slide-y-reverse-transition>

  <v-layout>
    <v-navigation-drawer v-model="drawer" location="right">
      <v-list style="height: calc(100% - 85px)">
        <v-container v-for="item in list" style="padding-bottom: 0">
          <v-card elevation="1" :disabled="loading" :loading="loading">
            <v-card-subtitle style="padding-top: 12px">
              <v-badge dot :color="item.mode === 'move' ? 'important' : '#00000000'" style="margin-right: 8px">
                <v-icon>{{item.icon}}</v-icon>
              </v-badge>
              {{item.name}}
            </v-card-subtitle>
            <v-card-actions>
              <v-btn color="important" @click="remove(item)">Remove</v-btn>
              <v-btn color="info" @click="paste(item)">Paste</v-btn>
            </v-card-actions>
          </v-card>
        </v-container>
      </v-list>
      <v-container style="position: sticky; bottom: 0">
        <v-card>
          <v-card-actions>
            <v-btn color="important" @click="clearAll">Clear All</v-btn>
            <v-btn color="info" @click="pasteAll">Paste All</v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-navigation-drawer>
  </v-layout>

  <v-dialog v-model="errDialog" persistent>
    <v-card>
      <v-card-title>Clipboard Error Log</v-card-title>
      <v-card-text style="max-height: 70vh; overflow-y: auto; padding-top: 0; color: red">
        {{errLog}}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="info" @click="errDialog = false">I see</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="popup" color="success" timeout="2000">
    <v-icon>mdi-check</v-icon>
    <span style="margin-left: 8px">Copied to clipboard</span>
  </v-snackbar>
</template>


<script>
import {clipBoard, syncToLocalStorage} from "@/system";
import {getFileIcon, getFileName, requestPasteItem} from "@/utils";

export default {
  name: "ClipBoard",
  props: ['path', 'show'],
  emits: ['paste'],
  data(){
    return {
      drawer: false,
      loading: false,
      list: [],

      errDialog: false,
      errLog: '',
      popup: false
    }
  },
  computed: {
    visible(){
      return this.list.length > 0
    },
  },
  methods: {
    updateList(){
      let result = []
      for(let key of Object.keys(clipBoard)){
        result.push({
          path: key,
          name: getFileName(key),
          icon: getFileIcon(clipBoard[key].type, key),
          mode: clipBoard[key].mode,
          time: clipBoard[key].time
        })
      }

      result.sort((a, b)=>{
        return b.time - a.time
      })
      this.list = result
    },
    clearAll(){
      for (let key of Object.keys(clipBoard)) {
        delete clipBoard[key]
      }
      syncToLocalStorage()
      this.updateList()
    },
    pasteAll(){
      this.loading = true
      let paths = []
      for (let key of Object.keys(clipBoard)) {
        paths.push(key)
      }
      requestPasteItem(paths, this.path).then(result => {
        let failed = result.filter(item => !item.success)
        if(failed.length > 0){
          this.errLog = failed.map(item => JSON.stringify(item)).join('\n')
          this.errDialog = true
        }
        this.updateList()
        this.$emit('paste')
      }).catch(err => {
        this.errLog = err.message
        this.errDialog = true
      }).finally(()=>{
        this.loading = false
      })
    },
    remove(item){
      delete clipBoard[item.path]
      syncToLocalStorage()
      this.updateList()
    },
    paste(item){
      this.loading = true
      requestPasteItem([item.path], this.path).then(result => {
        let failed = result.filter(item => !item.success)
        if(failed.length > 0){
          this.errLog = failed.map(item => JSON.stringify(item)).join('\n')
          this.errDialog = true
        }
        this.updateList()
        this.$emit('paste')
      }).catch(err => {
        this.errLog = err.message
        this.errDialog = true
      }).finally(()=>{
        this.loading = false
      })
    },
    toggleDrawer(){
      this.drawer = !this.drawer
    }
  }
}
</script>

<style scoped>
.float-btn{
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translate(-50%, -50%);

  z-index: 100;
}

</style>
