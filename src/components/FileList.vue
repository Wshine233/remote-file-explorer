<template id="body">
  <v-toolbar class="toolbar" color="primary" :elevation="2">
    <v-btn icon="mdi-menu"></v-btn>
    <v-toolbar-title>Files</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon="mdi-view-list"></v-btn>
    <v-btn icon="mdi-sort-variant"></v-btn>
    <v-btn icon="mdi-dots-vertical"></v-btn>
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

  <v-virtual-scroll id="list" item-height="60" :items="fileList">
    <template v-slot:default="{item, index}">
      <v-list-item variant="flat"
                   :title="item.name"
                   :value="item"
                   :subtitle="item.time"
                   density="comfortable"
                   height="60"
                   :class="{'user-select-disabled': true, 'item-selected': item.selected}"
                   @click="click(item)"
                   @touchstart="touchStart(item)"
                   @touchmove="touchMove"
                   @touchend="touchEnd">

        <template v-slot:prepend>
          <v-icon class="file-icon" style="margin-inline-end: 20px" :icon="getIcon(item.type, item.name)"
                  size="42"></v-icon>
        </template>

        <template v-slot:append>
          <v-btn variant="text" density="comfortable" icon="mdi-information" color="grey-lighten-1" @click.stop="clickInfo(item)"></v-btn>
        </template>

      </v-list-item>
    </template>
  </v-virtual-scroll>

  <v-overlay :model-value="loading"
             class="align-center justify-center"
             @click:outside="loading = false">
    <v-progress-circular
      color="primary"
      :indeterminate="true"
      size="64"
    ></v-progress-circular>
  </v-overlay>

  <v-dialog transition="dialog-bottom-transition"
  width="auto"
  v-model="dialog">
    <v-card>
      <v-card-text>
        {{dialogInfo.text}}
      </v-card-text>
    </v-card>
  </v-dialog>

  <v-slide-y-reverse-transition>
    <v-sheet v-if="selectMode" class="bottom-menu stay-top bottom-sticky">
      <v-btn variant="text" :stacked="true" size="small" density="comfortable">
        <v-icon>mdi-share</v-icon>
        <span>Share</span>
      </v-btn>

      <v-btn variant="text" :stacked="true" size="small" density="comfortable">
        <v-icon>mdi-file-move</v-icon>
        <span>Move</span>
      </v-btn>

      <v-btn variant="text" :stacked="true" size="small" density="comfortable">
        <v-icon>mdi-content-copy</v-icon>
        <span>Copy</span>
      </v-btn>

      <v-btn variant="text" :stacked="true" size="small" density="comfortable">
        <v-icon>mdi-delete</v-icon>
        <span>Delete</span>
      </v-btn>

      <v-btn variant="text" :stacked="true" size="small" density="comfortable">
        <v-icon>mdi-dots-horizontal</v-icon>
        <span>More</span>
      </v-btn>
    </v-sheet>
  </v-slide-y-reverse-transition>


</template>

<script>
import axios from "axios";
import {systemState} from "@/system";

export default {
  name: "FileList",
  data() {
    return {
      fileList: [
        {
          name: "Example Folder",
          type: 0,
          time: "2021-01-01 00:00:00",
          perm: "adxms",
          selected: false
        },
        {
          name: "Example File",
          type: 1,
          time: "2021-01-01 00:00:00",
          perm: "ad-ms",
          selected: false
        }
      ],
      pathBreadcrumb: [
        {
          name: 'root',
          path: '/'
        },
        {
          name: 'Example Folder',
          path: '/Example Folder'
        }
      ],
      selectMode: false,
      selectCount: 0,
      path: '/',
      loading: true,
      dialog: false,
      dialogInfo: {
        text: "这是放置详细信息的界面"
      }
    }
  },
  methods: {
    getIcon(type, name) {
      if (type === 0) {
        return "mdi-folder"
      } else if (name !== "") {
        return "mdi-file"
      }
    },
    changePath(path){
      this.getFileList(path)
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
    click(file) {
      if (this.selectMode) {
        this.updateSelect(file)
      } else {
        if (file.type === 0) {
          this.changePath(this.path + (this.path === '/' ? file.name : '/' + file.name))
        }
      }
    },
    updateSelect(file) {
      let cot = 0
      file.selected = !file.selected
      for (const file of this.fileList) {
        if (file.selected) {
          cot++;
        }
      }
      this.selectCount = cot
    },
    cancelSelect() {
      this.selectMode = false
      for (const file of this.fileList) {
        file.selected = false
      }
    },
    touchStart(file) {
      this.holdTimeout = setTimeout(() => {
        this.selectMode = true
        this.updateSelect(file)
      }, 700)
    },
    touchEnd() {
      clearTimeout(this.holdTimeout)
    },
    touchMove() {
      clearTimeout(this.holdTimeout)
    },
    clickInfo(file){
      this.dialog = true
      this.dialogInfo.text = `这是关于${file.name}的详细信息`
    },
    getFileList(path) {
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
            list.push({
              name: file.path.substr(file.path.lastIndexOf('/') + 1),
              type: file.type,
              time: "2021-01-01 00:00:00",
              perm: "adxms"
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
        } else {
          window.alert(res.message)
        }
      }).catch(err => {
        console.log(err)
        window.alert(err)
      })
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

.file-icon {
  width: 40px;
  margin-inline-end: 20px;
}

.breadcrumb-btn {
  min-width: 0;
  padding: 0 10px;
}

#list {
  /* 高度不超过屏幕底端 */
  max-height: calc(100vh - 112px);
}

.toolbar {
  position: sticky;
  top: 0;
  z-index: 10086;
}

.user-select-disabled {
  user-select: none;
}

.item-selected {
  background-color: #a0a0a0;
}

.breadcrumb-banner {
  position: relative;
  width: 100%;
  padding-left: 24px;
}

.stay-top{
  z-index: 10086;
}

.bottom-sticky{
  position: sticky;
  bottom: 0;
}

.bottom-menu{
  padding: 10px 10px;
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

  display: flex;
  align-items: center;
  justify-content: center;
}

.bottom-menu > *{
  flex-grow: 1;
}
</style>
