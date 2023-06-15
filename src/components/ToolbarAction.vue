<template>
  <v-sheet class="bottom-menu bottom-sticky" color="surface">
    <v-btn variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canShare" @click="showShare">
      <v-icon>mdi-share</v-icon>
      <span>Share</span>
    </v-btn>

    <v-btn variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canRename"
    @click="showRename">
      <v-icon>mdi-form-textbox</v-icon>
      <span>Rename</span>
    </v-btn>

    <v-btn variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canCopy" @click="addClipboard('copy')">
      <v-icon>mdi-content-copy</v-icon>
      <span>Copy</span>
    </v-btn>

    <v-btn variant="text" :stacked="true" size="small" density="comfortable" color="important" :disabled="!canDelete"
    @click="deleteConfirm = true">
      <v-icon>mdi-delete</v-icon>
      <span>Delete</span>
    </v-btn>

    <v-btn id="more" variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canMore">
      <v-icon>mdi-dots-horizontal</v-icon>
      <span>More</span>
      <v-menu activator="parent" z-index="10087">
        <v-list>
          <v-list-item v-if="selectList.length > 0" title="Download" value="download" density="comfortable" @click="download">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-download"
                      size="26"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Move" value="move" density="comfortable" :disabled="!canMove" @click="addClipboard('move')">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 12px" icon="mdi-file-move"
                      size="24"></v-icon>
            </template>
          </v-list-item>
          <v-list-item v-if="superUser" title="Set Permission" value="perm" density="comfortable" color="important" @click="showPermSet" :disabled="!canSetPerm">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-playlist-plus"
                      size="26" color="important"></v-icon>
            </template>
          </v-list-item>
          <v-list-item v-if="superUser" title="Add Ignore" value="perm" density="comfortable" color="important" @click="addIgnore" :disabled="!hasSelect">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-eye-remove"
                      size="26" color="important"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Select All" value="select-all" density="comfortable" @click="selectAll">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" size="26" color="warning">mdi-select-all</v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Select Invert" value="select-invert" density="comfortable" @click="selectInvert">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" size="26" color="warning">mdi-select-inverse</v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-btn>
  </v-sheet>

  <ShareDrawer ref="share" />

  <v-dialog v-model="deleteConfirm">
    <v-card>
      <v-card-title>Delete</v-card-title>
      <v-card-text>Are you sure to delete selected files?</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="deleteConfirm = false" :disabled="deleteLoading">Cancel</v-btn>
        <v-btn text color="important" @click="deleteSelected" :loading="deleteLoading">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <RenameFileDialog ref="rename" @confirm="renamed"/>
  <SetFilePermDialog ref="setPerm" @confirm="permSet"/>

  <v-snackbar v-model="popup" timeout="2000" color="error">{{errMsg}}</v-snackbar>
</template>

<script>
import axios from "axios";
import {clipBoard, syncToLocalStorage, systemState} from "@/system";
import ShareDrawer from "@/components/ShareDrawer";
import {addToClipboard, post} from "@/utils";
import RenameFileDialog from "@/components/RenameFileDialog";
import SetFilePermDialog from "@/components/SetFilePermDialog";

export default {
  name: "ToolbarAction",
  components: {SetFilePermDialog, RenameFileDialog, ShareDrawer},
  props: ['selectList', 'base', 'superUser'],
  emits: ['selectAll', 'selectInvert', 'delete', 'rename', 'permSet', 'copy-move', 'ignore'],
  data() {
    return {
      permission: '-----',
      errMsg: '',
      popup: false,

      deleteConfirm: false,
      deleteLoading: false
    }
  },
  computed: {
    hasSelect(){
      return this.selectList.length > 0
    },
    canShare() {
      return this.permission[4] === 's'
    },
    canMove() {
      return this.permission[3] === 'm' && this.permission[2] === 'x'
    },
    canCopy() {
      return this.permission[3] === 'm'
    },
    canDelete() {
      return this.permission[3] === 'm' && this.permission[2] === 'x'
    },
    canRename() {
      return this.permission[3] === 'm' && this.selectList.length === 1
    },
    canCreate() {
      //父文件夹的a
      return this.permission[0] === 'a'
    },
    canMore() {
      return true
    },
    canDownload() {
      return this.permission[1] === 'd'
    },
    canSetPerm(){
      return this.superUser && this.selectList.length === 1
    }
  },
  methods: {
    getParent() {
      return this.base
    },
    popupMsg(msg) {
      this.errMsg = msg
      this.popup = true
    },
    updatePermissions() {
      let perms = []
      for (let file of this.selectList) {
        perms.push(file.perm)
      }
      console.log(perms)
      this.mergePerms(perms)
    },
    mergePerms(perms) {
      let result = '*****'
      for (const perm of perms) {
        for (let i = 0; i < 5; i++) {
          if (result[i] === '-') {
            continue
          }
          result = result.substr(0, i) + perm[i] + result.substr(i + 1)
        }
      }
      this.permission = result
    },
    selectAll(){
      this.$emit('selectAll')
    },
    selectInvert(){
      this.$emit('selectInvert')
    },
    showShare(){
      this.$refs.share.show()
    },
    showRename(){
      this.$refs.rename.show(this.selectList[0])
    },
    showPermSet(){
      this.$refs.setPerm.show(this.selectList[0])
    },
    renamed(){
      this.$emit('rename')
    },
    permSet(){
      if(this.selectList.length !== 1){
        window.alert("暂不支持同时编辑多个文件的权限")
        return
      }
      this.$emit('permSet')
    },
    download(){
      if(this.selectList.length !== 1){
        window.alert("暂不支持同时下载多个文件")
        return
      }
      let file = this.selectList[0]
      if(file.type === 0){
        window.alert("暂不支持下载文件夹")
        return
      }

      post('/file/check-perm', {
        sessionId: systemState.currentSession,
        path: file.path,
        perm: 'd'
      }).then(res => {
        if(res.data){
          window.open(systemState.globalSettings.backendUrl + '/file/download?sessionId=' + systemState.currentSession + '&path=' + file.path)
        }else{
          this.popupMsg("You don't have permission to download this file.")
        }
      })
    },
    deleteSelected(){
      this.deleteLoading = true
      let paths = []
      for(let file of this.selectList){
        paths.push(file.path)
        delete clipBoard[file.path]
      }

      post('/file/delete', {
        sessionId: systemState.currentSession,
        paths: paths
      }).then(res => {
        this.$emit('delete')
        this.deleteConfirm = false
        this.deleteLoading = false
      }).catch(err => {
        this.deleteLoading = false
        this.popupMsg(err.message)
      })
    },
    addClipboard(mode){
      for (let file of this.selectList) {
        addToClipboard(file.path, file.type, mode)
      }
      syncToLocalStorage()
      this.$emit('copy-move')
    },
    addIgnore(){
      let list = this.selectList.map(file => file.path)

      post('/ignore/adds', {
        sessionId: systemState.currentSession,
        paths: list
      }).then(res => {
        this.$emit('ignore')
      }).catch(err => {
        this.popupMsg(err.message)
      })
    }
  },
  watch: {
    selectList() {
      this.updatePermissions()
      console.log("update")
    }
  },
  created() {
    this.updatePermissions()
  }
}
</script>

<style scoped>
.bottom-sticky {
  position: sticky;
  bottom: 0;
  z-index: 2;
}

.bottom-menu {
  padding: 10px 10px;
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

  display: flex;
  align-items: center;
  justify-content: center;
}

.bottom-menu > * {
  flex-grow: 1;
}
</style>
