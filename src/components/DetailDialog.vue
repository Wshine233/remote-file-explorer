<template>
  <v-dialog transition="dialog-bottom-transition"
            width="auto"
            v-model="dialog">
    <v-card>
      <v-card-title style="padding-bottom: 5px">Detail</v-card-title>
      <v-card-text style="padding-top: 0">
        <div v-for="group in info">
<!--          <v-list-subheader>{{ group.group }}</v-list-subheader>-->
          <v-list>
            <v-list-item v-for="info in group.attr" style="padding-left: 0; min-width: 80%">
              <template #title>
                <div style="padding-left: 0; min-width: 200px">
                  <v-list-item-subtitle>{{info.key}}</v-list-item-subtitle>
                  <v-list-item-title :class="{'clickable': info.click !== undefined}" @click="info.click !== undefined ? info.click() : ''">{{info.value}}</v-list-item-title>
                </div>
              </template>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>

    </v-card>
  </v-dialog>
</template>

<script>
import {systemState} from "@/system";
import {getReadableSize, getTimeStr} from "@/utils";
import axios from "axios";

export default {
  name: "DetailDialog",
  emits: ['path-click'],
  data(){
    return {
      dialog: false,
      file: {},
      fileInfo: {},
      info: [],
      dialogInfo: {
        text: "这是放置详细信息的界面"
      },
      show: false
    }
  },
  computed:{
  },
  methods: {
    requestInfo(){
      let paths = [this.fileInfo.path]
      let keys = ['permission', 'file_size', 'file_last_modified', 'file_last_accessed', 'file_created']
      let session = systemState.currentSession

      axios.defaults.baseURL = systemState.globalSettings.backendUrl
      axios.post('/file/info', {
        path: paths,
        keys: keys,
        sessionId: session
      }).then((res)=>{
        this.file = res.data.data[0]
        console.log(this.file)
        this.setInfo()
        this.dialog = true
      }).catch((err) => {
        this.fileInfo = {}
        this.file = {}
        this.dialog = false
        this.show = false
        window.alert(err)
      })
    },
    clickPath(path){
      this.$emit('path-click', path)
      this.dialog = false
    },
    setInfo() {
      let parent = this.fileInfo.path.substr(0, this.fileInfo.path.lastIndexOf('/'))
      parent = parent.length === 0 ? '/' : parent
      if(this.fileInfo.type === 0){
        this.info = [
          {
            group: 'Basic Info',
            attr: [
              {
                key: "Name",
                value: this.fileInfo.name
              },
              {
                key: "Path",
                value: parent,
                click: () => {
                  this.clickPath(parent)
                }
              },
              {
                key: "Type",
                value: 'Folder'
              },
              {
                key: "Last Modified",
                value: getTimeStr(this.file.file_last_modified)
              },
              {
                key: "Created",
                value: getTimeStr(this.file.file_created)
              },
              {
                key: 'Permission',
                value: this.file.permission === null ? '-----' : this.file.permission
              }
            ]
          }
        ]
        return
      }
      this.info = [
        {
          group: 'Basic Info',
          attr: [
            {
              key: "Name",
              value: this.fileInfo.name
            },
            {
              key: "Path",
              value: parent,
              click: () => {
                this.clickPath(parent)
              }
            },
            {
              key: "Size",
              value: getReadableSize(parseInt(this.file.file_size))
            },
            {
              key: "Type",
              value: 'File'
            },
            {
              key: "Last Modified",
              value: getTimeStr(this.file.file_last_modified)
            },
            {
              key: "Created",
              value: getTimeStr(this.file.file_created)
            },
            {
              key: 'Permission',
              value: this.file.permission
            }
          ]
        }
      ]
    },
  },
  watch: {
    show(val){
      if(val && this.fileInfo.path !== undefined){
        this.requestInfo()
      }
    },
    dialog(val){
      this.show = val
    }
  }

}
</script>

<style scoped>
.clickable{
  cursor: pointer;
  color: #1890ff;
  text-decoration: underline;
}
</style>
