<template>
  <v-sheet class="bottom-menu bottom-sticky" color="surface">
    <v-btn variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canShare">
      <v-icon>mdi-share</v-icon>
      <span>Share</span>
    </v-btn>

    <v-btn variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canMove">
      <v-icon>mdi-form-textbox</v-icon>
      <span>Rename</span>
    </v-btn>

    <v-btn variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canCopy">
      <v-icon>mdi-content-copy</v-icon>
      <span>Copy</span>
    </v-btn>

    <v-btn variant="text" :stacked="true" size="small" density="comfortable" color="important" :disabled="!canDelete">
      <v-icon>mdi-delete</v-icon>
      <span>Delete</span>
    </v-btn>

    <v-btn id="more" variant="text" :stacked="true" size="small" density="comfortable" :disabled="!canMore">
      <v-icon>mdi-dots-horizontal</v-icon>
      <span>More</span>
      <v-menu activator="parent" z-index="10087">
        <v-list>
          <v-list-item title="Download" value="download" density="comfortable">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-download"
                      size="26"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Move" value="move" density="comfortable">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 12px" icon="mdi-file-move"
                      size="24"></v-icon>
            </template>
          </v-list-item>
          <v-list-item title="Set Permission" value="perm" density="comfortable" color="important">
            <template v-slot:prepend>
              <v-icon style="margin-inline-end: 10px" icon="mdi-playlist-plus"
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


</template>

<script>
import axios from "axios";
import {systemState} from "@/system";

export default {
  name: "ToolbarAction",
  props: ['selectList', 'base'],
  emits: ['selectAll', 'selectInvert'],
  data() {
    return {
      permission: '-----'
    }
  },
  computed: {
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
      return this.permission[3] === 'm'
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
    }
  },
  methods: {
    getParent() {
      return this.base
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
  z-index: 10086;
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
