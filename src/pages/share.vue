<template>
  <SortSelectDialog ref="sortSelector" />

  <v-scroll-y-transition >
    <v-sheet class="overlay" v-if="protected">
      <v-expand-transition>
        <div class="overlay-center elevation-3" v-if="!transitioning">
          <div class="overlay-title">This Sharing is protected by a password</div>
          <v-text-field></v-text-field>
          <v-btn @click="confirmPassword">Confirm</v-btn>
        </div>
      </v-expand-transition>
      <v-expand-transition>
        <div class="overlay-center elevation-3" v-if="transitioning">
          <v-icon color="success" size="xx-large" style="align-self: center">mdi-check-circle-outline</v-icon>
        </div>
      </v-expand-transition>
    </v-sheet>
  </v-scroll-y-transition>

  <div v-if="!protected">
    <v-toolbar class="toolbar" color="success" :elevation="2">
      <v-toolbar-title>Shared from {{shareFrom}}</v-toolbar-title>

      <v-btn icon="mdi-sort-variant" @click="showSortSelector"></v-btn>
      <template v-slot:extension>
        <v-breadcrumbs v-if="!selectMode" class="overflow-x-auto"
                       :items="breadCrumbs"
                       density="comfortable">
          <template v-slot:title="{ item }">
            <v-btn class="breadcrumb-btn" variant="text" size="small" density="comfortable" @click="openPath(item.path)">{{ item.name }}</v-btn>
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

    <ShareListView :share-list="shares" :select-mode="selectMode" @clickInfo="clickInfo" @clickItem="click" @holdItem="hold"/>

    <v-overlay :model-value="loading"
               class="align-center justify-center"
               @click:outside="loading = false">
      <v-progress-circular
        color="primary"
        :indeterminate="true"
        size="64"
      ></v-progress-circular>
    </v-overlay>
  </div>


  <DetailDialog ref="detail" />
</template>

<script>
import FileListView from "@/components/FileListView";
import DetailDialog from "@/components/DetailDialog";
import ToolbarAction from "@/components/ToolbarAction";
import SortSelectDialog from "@/components/SortSelectDialog";
import ShareListView from "@/components/ShareListView";
import {getDateStr, getReadableSize} from "@/utils";
export default {
  name: "SharePage",
  components: {ShareListView, SortSelectDialog, ToolbarAction, DetailDialog, FileListView},
  data(){
    return {
      shareFrom: "Wshine",
      protected: true,
      transitioning: false,
      shares: [
        {
          name: "Example Folder",
          type: 0,
          time: 1008600,
          timeStr: "2021-01-01 12:00:00",
          perm: '-d---',
          selected: false
        },
        {
          name: "Example File",
          type: 1,
          size: 4096,
          time: 1008600,
          timeStr: "2021-01-01 12:00:00",
          perm: '-d---',
          selected: false
        }
      ],
      breadCrumbs: [
        {
          name: "share",
          path: "/"
        },
        {
          name: "Example Folder",
          path: "/Example Folder"
        }
      ],
      selectMode: false,
    }
  },
  methods:{
    confirmPassword(){
      this.transitioning = true
      setTimeout(() => {
        this.protected = false
        this.transitioning = false
      }, 1000)
    },
    openPath(name){
      let path = ''
      for (let i = 1; i < this.breadCrumbs; i++){
        path += '/' + this.breadCrumbs[i].path
      }
      path += '/' + name
    },
    listFile(id, path){
      for(let i = 0; i < this.shares.length; i++){
        this.shares[i].timeStr = getDateStr(this.shares[i].time)
        this.shares[i].sizeStr = getReadableSize(this.shares[i].size)
      }
    },
    updateBreadCrumbs(id, path){
      let res = [
        {
          name: "share",
          path: "/"
        }
      ]

      let pathList = path.split('/')
      let pathStr = ''
      for (const pathItem of pathList) {
        if(pathItem === '') continue
        pathStr += '/' + pathItem
        res.push({
          name: pathItem,
          path: pathStr
        })
      }

      this.breadCrumbs = res
    },
    showSortSelector(){
      this.$refs.sortSelector.show()
    },
    cancelSelect() {
      this.selectMode = false
      for (const file of this.fileList) {
        file.selected = false
      }
    },
    showDetail(file){
      this.$refs.detail.fileInfo = {
        path: this.path + (this.path === '/' ? file.name : '/' + file.name),
        type: file.type,
        name: file.name
      }
      this.$refs.detail.show = true
    },
    getShareId(){

    }
  },
  created() {
    this.listFile(this.getShareId(), '/')
    this.updateBreadCrumbs(this.getShareId(), '/')
  }
}
</script>

<style scoped>
.overlay{
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #4CAF50;

  z-index: 10086;
}

.overlay-center{
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  min-width: 300px;
  max-width: 90%;
  background-color: #fafafa;
  border-radius: 10px;
  padding: 20px;

  display: flex;
  flex-direction: column;
}

.overlay-title{
  font-size: 20px;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
}
</style>
