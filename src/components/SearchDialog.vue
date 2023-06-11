<template>
  <v-dialog
    v-model="dialog"
    fullscreen
    :scrim="false"
    transition="dialog-bottom-transition">
    <v-card class="fill-height">
      <v-toolbar color="primary" dense floating>
        <v-btn v-if="!focus" icon @click="close" density="comfortable">
          <v-icon>mdi-close</v-icon>
        </v-btn>

        <v-text-field v-model="keyword" class="search-input" label="Search..." hide-details single-line
                      @focusin="focus = true" @focusout="focus = false"></v-text-field>

        <v-btn v-if="!focus" icon density="comfortable" @click="showFilter">
          <v-icon>mdi-filter-variant</v-icon>
        </v-btn>
      </v-toolbar>
      <v-progress-linear v-if="loading" indeterminate color="warning" height="5"></v-progress-linear>

      <FileListView v-if="!focus && !loading" :file-list="list" :select-mode="false" @clickItem="clickItem" @clickInfo="clickInfo" @holdItem="holdItem" />

    </v-card>
  </v-dialog>

  <v-lazy>
    <FilterDialog ref="filter" @save="updateFilter" />
  </v-lazy>

  <DetailDialog ref="detail" @path-click="pathClick" />

  <v-snackbar v-model="popup" color="error" timeout="2000">
    Error: {{errorText}}
  </v-snackbar>

</template>


<script>
import {systemState} from "@/system";
import MountWindow from "@/components/MountWindow";
import UserWindow from "@/components/UserWindow";
import PermWindow from "@/components/PermWindow";
import FileListView from "@/components/FileListView";
import FilterDialog from "@/components/FilterDialog";
import axios from "axios";
import {getDateStr, getReadableSize} from "@/utils";
import DetailDialog from "@/components/DetailDialog";

export default {
  name: "SearchDialog",
  props: ['path'],
  emits: ['preview', 'path-click'],
  components: {FilterDialog, FileListView, PermWindow, UserWindow, MountWindow, DetailDialog},
  data() {
    return {
      dialog: false,
      focus: false,
      keyword: '',
      fileList: [],
      loading: false,
      filter: {},
      first: true,

      errorText: '',
      popup: false
    }
  },
  computed: {
    list(){
      let result = []
      for(let i = 0; i < this.fileList.length; i++){
        let file = this.fileList[i]
        result.push({
          name: file.name,
          path: file.path,
          type: file.type,
          time: file.time_modified,
          timeStr: getDateStr(file.time_modified),
          size: file.size,
          sizeStr: getReadableSize(file.size),
          selected: file.selected
        })
      }
      return result
    }
  },
  methods:{
    show(){
      this.dialog = true
      this.filter = {
        folder: this.path,
        recursive: false
      }
    },
    close(){
      this.dialog = false
    },
    showFilter(){
      this.$refs.filter.show(this.filter)
    },
    updateFilter(filter){
      this.filter = filter
      console.log(this.filter)
      this.findFile()
    },
    clickItem(item){
      if(item.type === 0){
        this.$emit('path-click', item.path)
        this.dialog = false
        return
      }
      this.$emit('preview', item)
    },
    clickInfo(file){
      this.$refs.detail.fileInfo = {
        path: file.path,
        type: file.type,
        name: file.name
      }
      this.$refs.detail.show = true
    },
    holdItem(item){

    },
    pathClick(path){
      this.$emit('path-click', path)
      this.dialog = false
    },
    findFile(){
      if(this.keyword.length === 0){
        return
      }
      this.loading = true

      axios.defaults.baseURL = systemState.globalSettings.backendUrl
      axios.post('/file/search', {
        sessionId: systemState.currentSession,
        keyword: this.keyword,
        filter: this.filter,
        limit: 500, //目前无作用，意义是限制搜索结果数量，但未对接用于解决不显示所有结果的问题
      }).then(res => {
        console.log('search result', res.data)
        let data = res.data
        if(data.success){
          this.fileList = data.data
          this.loading = false
          return
        }
        this.errorText = data.message
        this.popup = true
        this.loading = false
      }).catch(err => {
        this.errorText = err
        this.popup = true
        this.loading = false
      })

    }
  },
  watch: {
    dialog(val){
      if(val){

      }
    },
    focus(val){
      if(!val){
        this.findFile()
      }
    }
  }
}
</script>

<style scoped>
.search-input{
  padding-inline-start: 10px;
  padding-inline-end: 10px;
}
</style>
