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

        <v-text-field class="search-input" label="Search..." hide-details single-line clearable
                      @focusin="focus = true" @focusout="focus = false"></v-text-field>

        <v-btn v-if="!focus" icon density="comfortable" @click="showFilter">
          <v-icon>mdi-filter-variant</v-icon>
        </v-btn>
      </v-toolbar>

      <FileListView :file-list="fileList" :select-mode="false" />

    </v-card>
  </v-dialog>

  <v-lazy>
    <FilterDialog ref="filter" />
  </v-lazy>

</template>


<script>
import {systemState} from "@/system";
import MountWindow from "@/components/MountWindow";
import UserWindow from "@/components/UserWindow";
import PermWindow from "@/components/PermWindow";
import FileListView from "@/components/FileListView";
import FilterDialog from "@/components/FilterDialog";

export default {
  name: "SearchDialog",
  components: {FilterDialog, FileListView, PermWindow, UserWindow, MountWindow},
  data() {
    return {
      dialog: false,
      focus: false,
      fileList: []
    }
  },
  computed: {

  },
  methods:{
    close(){
      this.dialog = false
    },
    showFilter(){
      this.$refs.filter.dialog = true
    }
  },
  watch: {
    dialog(val){
      if(val){

      }
    },
    focus(val){
      //TODO: 当脱离Focus状态后，根据搜索框中的关键字查找文件，不可以空值
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
