<template>
  <v-window-item value="mount" class="fill-height">
    <v-card class="fill-height">
      <v-toolbar
        dark
        color="primary"
      >
        <v-btn icon dark @click="back">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title>Mount Settings</v-toolbar-title>
      </v-toolbar>
      <v-container>
        <v-card>
          <v-card-title>
            <div class="flex-inline">
              Mount List
              <v-spacer></v-spacer>
              <v-btn density="comfortable" :variant="loadingMount ? 'text' : 'outlined'" color="success"
                     class="rect-btn-outlined" :loading="loadingMount" @click="showAddMount">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="item in mountList" :value="item.root" rounded>
                <v-list-item-title class="ellipse-rtl">{{ item.root }}</v-list-item-title>
                <v-list-item-subtitle class="ellipse-rtl">{{ item.target }}</v-list-item-subtitle>
                <template #append>
                  <v-btn color="important" density="comfortable" min-width="10" @click.stop="remove(item.origin)"
                         :disabled="loadingMount">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>
      <v-container>
        <v-card>
          <v-card-title>
            <div class="flex-inline">
              Ignore List
              <v-spacer></v-spacer>
              <v-btn density="comfortable" :variant="loadingIgnore ? 'text' : 'outlined'" color="success"
                     class="rect-btn-outlined" :loading="loadingIgnore" @click="showAddIgnore">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-title>

          <v-card-text>
            <v-list>
              <v-list-item v-for="item in ignoreList" :value="item.path" @click="edit(item)" rounded>
                <v-list-item-title class="ellipse-rtl">{{ item.path }}</v-list-item-title>
                <template #append>
                  <v-btn color="important" density="comfortable" min-width="10" @click.stop="removeIgnore(item.origin)"
                         :disabled="loadingIgnore">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>
    </v-card>
  </v-window-item>

  <AddMountDialog ref="addMount" @confirm="fetchData"/>
  <AddIgnoreDialog ref="addIgnore" @confirm="fetchData"/>

  <ConfirmDialog ref="confirm"/>
  <v-snackbar v-model="popup" timeout="3000" color="error">
    {{ popupText }}
  </v-snackbar>
</template>

<script>
import ConfirmDialog from "@/components/ConfirmDialog";
import {systemState} from "@/system";
import {post} from "@/utils";
import AddMountDialog from "@/components/AddMountDialog";
import AddIgnoreDialog from "@/components/AddIgnoreDialog";

export default {
  name: "MountWindow",
  components: {AddIgnoreDialog, AddMountDialog, ConfirmDialog},
  emits: ['back'],
  data() {
    return {
      loadingMount: true,
      loadingIgnore: true,
      mounts: [] /*[
        {
          target: 'D:/Example File/Example Executive File.exe',
          root: '/Example File.exe'
        },
        {
          target: 'D:/Example Folder',
          root: '/Example Folder'
        },
      ]*/,
      ignores: [], //['D:/test ignore/ignore folder/ignore file.txt'],

      popup: false,
      popupText: '',
    }
  },
  computed: {
    mountList() {
      let res = []
      for (const mount of this.mounts) {
        res.push({
          origin: mount,
          target: this.reverseStr(mount.target),
          root: this.reverseStr(mount.root)
        })
      }
      return res
    },
    ignoreList() {
      let res = []
      for (let i = 0; i < this.ignores.length; i++) {
        let ignore = this.ignores[i].toString()
        res.push({
          origin: ignore,
          path: this.reverseStr(ignore)
        })
      }
      return res
    }
  },
  methods: {
    popupShow(text) {
      this.popupText = text
      this.popup = true
    },
    show() {
      this.loading = true
      this.fetchData()
    },
    back() {
      this.$emit('back')
    },
    reverseStr(text) {
      const findList = '[]【】()（）{}<>《》'
      const replaceList = '][】【)）(}{><》《'
      text = text.split('').reverse().join('')
      let result = []
      for (let i = 0; i < text.length; i++) {
        let char = text[i]
        let index = findList.indexOf(char)
        if (index !== -1) {
          result.push(replaceList[index])
        } else {
          result.push(char)
        }
      }

      return result.join('')
    },
    remove(mount) {
      this.showConfirm('Warning', 'Are you sure to remove this mount?\nThis will not delete the file/folder in the target path.', true,
        res => {
          if (res) {
            this.loadingMount = true
            post('/mount/remove', {
              sessionId: systemState.currentSession,
              root: mount.root
            }).then(res => {
              this.fetchData()
            }).catch(res => {
              this.popupShow(res.message)
              this.loadingMount = false
            })
          }
        })
    },
    removeIgnore(ignore) {
      this.showConfirm('Warning', 'Are you sure to remove the ignore?\nThis file/folder may be mounted and visible for other users.',
        true, res => {
          if (res) {
            this.loadingIgnore = true
            post('/ignore/remove', {
              sessionId: systemState.currentSession,
              target: ignore
            }).then(res => {
              this.fetchData()
            }).catch(res => {
              this.popupShow(res.message)
              this.loadingIgnore = false
            })
          }
        })
    },
    showConfirm(title = 'Warning', content = 'Are you sure to remove this item?', warn = true, callback = null) {
      this.$refs.confirm.show(title, content, warn, callback)
    },
    showAddMount(){
      this.$refs.addMount.show()
    },
    showAddIgnore(){
      this.$refs.addIgnore.show()
    },
    fetchData() {
      post('/mount', {
        sessionId: systemState.currentSession
      }).then(res => {
        this.mounts = res.data
      }).catch(res => {
        this.popupShow(res.message)
      }).finally(() => {
        this.loadingMount = false
      })

      post('/ignore', {
        sessionId: systemState.currentSession
      }).then(res => {
        this.ignores = res.data
      }).catch(res => {
        this.popupShow(res.message)
      }).finally(() => {
        this.loadingIgnore = false
      })
    }
  }
}
</script>

<style scoped>
.flex-inline {
  display: flex;
  justify-content: left;
  align-items: center;
}

.rect-btn-outlined {
  min-width: 0;
  padding: 0 4px;
}

.ellipse-rtl {
  padding-right: 16px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  direction: rtl;
  text-align: left;
  unicode-bidi: bidi-override;
}
</style>
