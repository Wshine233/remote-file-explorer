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

      <FileListView v-if="!focus && !loading" :file-list="fileList" :select-mode="false" />

    </v-card>
  </v-dialog>

  <v-lazy>
    <FilterDialog ref="filter" @save="updateFilter" />
  </v-lazy>

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

export default {
  name: "SearchDialog",
  props: ['path'],
  components: {FilterDialog, FileListView, PermWindow, UserWindow, MountWindow},
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
