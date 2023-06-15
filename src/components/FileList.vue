<template id="body">
  <UserDrawer ref="userDrawer" :user-info="userInfo"/>
  <SortSelectDialog ref="sortSelector" @confirm="updateSortRule"/>
<!--  <ViewSelectDialog ref="viewSelector" />-->
  <Settings ref="setting" />
  <SearchDialog ref="search" :path="path" @path-click="clickPath" @preview="file => tryPreview(file)" />

  <v-toolbar class="toolbar" color="primary" :elevation="2">
    <v-btn icon="mdi-menu" @click="showDrawer"></v-btn>
    <v-toolbar-title>Files</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon="mdi-magnify" @click="showSearch"></v-btn>
    <v-btn icon="mdi-sort-variant" @click="showSortSelector"></v-btn>
    <v-btn icon="mdi-dots-vertical">
      <v-icon>mdi-dots-vertical</v-icon>
      <v-menu activator="parent" z-index="10087">
        <v-list>
          <v-list-item title="Refresh" value="refresh" density="comfortable" @click="changePath(path)">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-refresh"
                      size="26"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Create Folder" value="download" density="comfortable" @click="showCreateFolder">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-folder-plus-outline"
                      size="26"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Upload File" value="upload" density="comfortable" @click="showUpload">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-upload"
                      size="26"></v-icon>
            </template>
          </v-list-item>
          <v-list-item v-if="superUser" title="Add Mount" value="move" density="comfortable" @click="showAddMount">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-plus-box-outline"
                      size="26"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Settings" value="settings" density="comfortable" color="important" @click="showSettings">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-cog"
                      size="26"></v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-btn>
    <template v-slot:extension>
      <v-breadcrumbs v-if="!selectMode" class="overflow-x-auto"
                     :items="pathBreadcrumb"
                     density="comfortable">
        <template v-slot:title="{ item }">
          <v-btn class="breadcrumb-btn" variant="text" size="small" density="comfortable" @click="changePath(item.path)">{{ item.name }}</v-btn>
        </template>
        <template v-slot:divider>
          <div>/</div>
        </template>
      </v-breadcrumbs>
      <div v-else class="breadcrumb-banner">
        <span class="font-weight-bold">{{ selectCount }} file(s) selected.</span>
        <v-btn @click="cancelSelect" style="position: absolute; top: 50%; right: 13px; transform: translate(0, -50%)"
               icon="mdi-close" size="small"></v-btn>
      </div>

    </template>
  </v-toolbar>

  <FileListView :file-list="list" :select-mode="selectMode" @clickInfo="clickInfo" @clickItem="click" @holdItem="hold"/>

  <v-overlay :model-value="loading"
             class="align-center justify-center"
             @click:outside="loading = false">
    <v-progress-circular
      color="primary"
      :indeterminate="true"
      size="64"
    ></v-progress-circular>
  </v-overlay>

  <DetailDialog ref="detail" />

  <div style="position: sticky; bottom: 0; background-color: transparent">
    <AudioPreviewer ref="audioPreview" :src="previewSrc"/>
    <ToolbarAction :select-list="selectList" :base="path" ref="actions" :super-user="superUser" :visible="selectMode"
                   @selectAll="selectAll" @selectInvert="selectInvert"
                   @delete="changePath(path)" @rename="changePath(path)" @permSet="changePath(path)" @copy-move="updateCopyMove" @ignore="changePath(path)"/>
  </div>

  <ImagePreviewDialog ref="imgPreview" :src="previewSrc"/>
  <VideoPreviewDialog ref="videoPreview" :src="previewSrc"/>
  <TextPreviewDialog ref="textPreview" :src="previewSrc"/>

  <CreateFolderDialog ref="createFolder" @confirm="changePath(path)" :path="path"/>
  <AddMountDialog ref="addMount" @confirm="changePath(path)" :path="path"/>
  <UploadFileDialog ref="upload" @confirm="changePath(path)" :root="path"/>

  <ClipBoard ref="clipboard" :path="path" :show="!selectMode" @paste="changePath(path)"/>

  <v-snackbar v-model="popup" color="error" timeout="2000">
    {{errMsg}}
  </v-snackbar>

</template>

<script>
import axios from "axios";
import {systemState} from "@/system";
import {checkSuperUser, getDateStr, getFileExtType, getReadableSize, getTimeStr, sortByFileName} from "@/utils";
import ToolbarAction from "@/components/ToolbarAction";
import FileListView from "@/components/FileListView";
import UserDrawer from "@/components/UserDrawer";
import ViewSelectDialog from "@/components/ViewSelectDialog";
import SortSelectDialog from "@/components/SortSelectDialog";
import DetailDialog from "@/components/DetailDialog";
import Settings from "@/components/Settings";
import SearchDialog from "@/components/SearchDialog";
import ImagePreviewDialog from "@/components/ImagePreviewDialog";
import VideoPreviewDialog from "@/components/VideoPreviewDialog";
import AudioPreviewer from "@/components/AudioPreviewer";
import TextPreviewDialog from "@/components/TextPreviewDialog";
import CreateFolderDialog from "@/components/CreateFolderDialog";
import ClipBoard from "@/components/ClipBoard";
import AddMountDialog from "@/components/AddMountDialog";
import UploadFileDialog from "@/components/UploadFileDialog";

export default {
  name: "FileList",
  components: {
    UploadFileDialog,
    AddMountDialog,
    ClipBoard,
    CreateFolderDialog,
    TextPreviewDialog,
    AudioPreviewer,
    VideoPreviewDialog,
    ImagePreviewDialog,
    SearchDialog,
    Settings, DetailDialog, SortSelectDialog, ViewSelectDialog, UserDrawer, FileListView, ToolbarAction},
  data() {
    return {
      fileList: [], /*[
        {
          name: "Example Folder",
          type: 0,
          time: 1111,
          timeStr: "2021-01-01 00:00:00",
          selected: false
        },
        {
          name: "Example File",
          type: 1,
          time: 1111,
          timeStr: "2021-01-01 00:00:00",
          selected: false
        }
      ],*/
      userInfo: {
        name: 'Wshine',
        group: 'admin'
      },
      superUser: false,
      pathBreadcrumb: [
        {
          name: 'root',
          path: '/'
        }
      ],
      selectMode: false,
      selectList: [],
      path: '/',
      loading: true,
      dialog: false,
      dialogInfo: {
        text: "这是放置详细信息的界面"
      },
      drawer: false,
      fileInfo: null,
      sortRule: {
        sort: sortByFileName,
        descending: false,
        blockTypes: []
      },

      previewSrc: '',

      errMsg: '',
      popup: false
    }
  },
  computed:{
    list(){
      let list = this.fileList.filter(item => {
        let ext = item.name.substr(item.name.lastIndexOf('.'))
        ext = getFileExtType(ext, item.type)
        if(this.sortRule.blockTypes.includes(ext)){
          return false
        }

        return true
      })

      this.sortRule.sort(list)
      if(this.sortRule.descending){
        list = list.reverse();
      }

      return list
    },
    selectCount(){
      return this.selectList.length
    }
  },
  methods: {
    updateCopyMove(){
      this.$refs.clipboard.updateList()
      this.setSelectMode(false)
    },
    changePath(path, callback){
      this.setSelectMode(false)
      this.getFileList(path, callback)
      this.checkSuper()
      this.updateCopyMove()
    },
    checkSuper(){
      checkSuperUser().then(res => {
        this.superUser = res
      }).catch(err => {
        console.log('failed to check super user: ', err.message)
      })
    },
    updatePathBreadcrumb(){
      let list = []
      let path = this.path
      while (path !== '/' && path !== '') {
        let name = path.substr(path.lastIndexOf('/') + 1)
        list.push({
          name: name,
          path: path
        })
        path = path.substr(0, path.lastIndexOf('/'))
      }
      list.push({
        name: 'root',
        path: '/'
      })
      list.reverse()
      this.pathBreadcrumb = list
    },
    tryPreview(file){
      console.log('preview: ', file)
      let type = getFileExtType(file.name.substr(file.name.lastIndexOf('.')), file.type)

      axios.defaults.baseURL = systemState.globalSettings.backendUrl
      axios.post('/preview/token', {
        sessionId: systemState.currentSession,
        path: file.path
      }).then(res => {
        console.log(res)
        let data = res.data
        if(!data.success){
          this.showErr(data.message)
          return
        }
        let token = data.data
        this.previewSrc = systemState.globalSettings.backendUrl + '/preview?token=' + token + '&user=' + systemState.currentSession
        switch (type) {
          case 'picture':
            this.$refs.imgPreview.show()
            break
          case 'video':
            this.$refs.videoPreview.show()
            break
          case 'audio':
            let stem = file.name.substr(0, file.name.lastIndexOf('.'))
            this.$refs.audioPreview.show(stem, '')
            break
          case 'text':
            this.$refs.textPreview.show()
            break
        }

      }).catch(err => {
        console.log(err)
        this.showErr(err.data.message)
      })

    },
    click(file) {
      if (this.selectMode) {
        this.updateSelect(file)
      } else {
        if (file.type === 0) {
          this.changePath(this.path + (this.path === '/' ? file.name : '/' + file.name))
        }else{
          this.tryPreview(file)
        }
      }
    },
    hold(file){
      if(this.selectMode) return
      this.setSelectMode()
      this.updateSelect(file)
    },
    setSelectMode(enable = true){
      this.selectMode = enable

      if(!enable){
        this.cancelSelect()
      }
    },
    updateSelect(file) {
      file.selected = !file.selected
      let selectList = this.getSelectList()
      this.selectList = selectList
      // this.selectCount = selectList.length
    },
    getSelectList(){
      let result = []
      for (const file of this.fileList) {
        if (file.selected) {
          result.push(file)
        }
      }
      return result
    },
    cancelSelect() {
      this.selectMode = false
      for (const file of this.fileList) {
        file.selected = false
      }
    },
    selectPath(path){
      this.setSelectMode()
      for (const file of this.fileList) {
        if(file.path === path){
          this.updateSelect(file)
        }
      }
    },
    clickInfo(file){
      this.showDetail(file)
    },
    clickPath(parent, path){
      this.changePath(parent, () => {
        if(path){
          this.selectPath(path)
        }
      })
    },
    showErr(msg){
      this.errMsg = msg
      this.popup = true
    },
    showDrawer(){
      this.$refs.userDrawer.drawer = true
    },
    /*showViewSelector(){
      this.$refs.viewSelector.dialog = true
    },*/
    showSortSelector(){
      this.$refs.sortSelector.dialog = true
    },
    showDetail(file){
      this.$refs.detail.fileInfo = {
        path: this.path + (this.path === '/' ? file.name : '/' + file.name),
        type: file.type,
        name: file.name
      }
      this.$refs.detail.show = true
    },
    showSettings(){
      this.$refs.setting.dialog = true
    },
    showSearch(){
      this.$refs.search.show()
    },
    showCreateFolder(){
      this.$refs.createFolder.show()
    },
    showAddMount(){
      this.$refs.addMount.show()
    },
    showUpload(){
      this.$refs.upload.show()
    },
    selectAll(){
      for (const file of this.fileList) {
        file.selected = true
      }
      this.selectList = this.getSelectList()
      // this.selectCount = this.selectList.length
    },
    selectInvert(){
      for (const file of this.fileList) {
        file.selected = !file.selected
      }
      this.selectList = this.getSelectList()
      // this.selectCount = this.selectList.length
    },
    getFileList(path, callback) {
      this.loading = true
      console.log(`正在获取${path}下的文件列表`)
      axios.defaults.baseURL = systemState.globalSettings.backendUrl
      axios.post('/file/list-file', {
        sessionId: systemState.currentSession,
        path: path,
      }).then(res => {
        console.log(res)
        res = res.data
        let list = []
        if (res.success) {
          for (let file of res.data) {
            let time = 'unknown'
            if(file.time !== null){
              time = getDateStr(file.time)
            }
            list.push({
              name: file.path.substr(file.path.lastIndexOf('/') + 1),
              path: file.path,
              type: file.type,
              time: file.time,
              size: file.type === 0 ? 0 : file.size,
              timeStr: time,
              sizeStr: file.type === 0 ? '' : getReadableSize(file.size),
              perm: file.perm
            })
          }
          if(!this.loading){
            return
          }
          this.path = path
          window.location.href = "#/file?path=" + path
          this.fileList = list
          this.updatePathBreadcrumb()
          this.loading = false

          if(callback){
            callback()
          }
        } else {
          window.alert(res.message)
          if(res.message.includes("login")){
            window.location.href = '/login.html'
          }
        }
      }).catch(err => {
        console.log(err)
        window.alert(err)
      })
    },
    updateSortRule(rule){
      this.sortRule = rule
    }
  },
  watch: {
    drawer(newValue){
      this.$refs.userDrawer.drawer = newValue
    }
  }
}
</script>

<style scoped>
#body {
  width: 100%;
  height: 100%;
  position: relative;
}

*{
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.breadcrumb-btn {
  min-width: 0;
  padding: 0 10px;
}

.toolbar {
  position: sticky;
  top: 0;
  z-index: 2;
}

.breadcrumb-banner {
  position: relative;
  width: 100%;
  padding-left: 24px;
}

.stay-top{
  z-index: 10086;
}
</style>
