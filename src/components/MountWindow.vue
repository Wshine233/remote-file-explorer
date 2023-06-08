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
              <v-btn density="comfortable" variant="outlined" color="success" class="rect-btn-outlined">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="item in mountList" :value="item.root" @click="edit(item)" rounded>
                <v-list-item-title class="ellipse-rtl">{{item.root}}</v-list-item-title>
                <v-list-item-subtitle class="ellipse-rtl">{{item.target}}</v-list-item-subtitle>
                <template #append>
                  <v-btn color="important" density="comfortable" min-width="10" @click.stop="remove(item)">
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
              <v-btn density="comfortable" variant="outlined" color="success" class="rect-btn-outlined">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-title>

          <v-card-text>
            <v-list>
              <v-list-item v-for="item in ignoreList" :value="item.path" @click="edit(item)" rounded>
                <v-list-item-title class="ellipse-rtl">{{item.path}}</v-list-item-title>
                <template #append>
                  <v-btn color="important" density="comfortable" min-width="10" @click.stop="removeIgnore(item)">
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

  <ConfirmDialog ref="confirm" />
</template>

<script>
import ConfirmDialog from "@/components/ConfirmDialog";
export default {
  name: "MountWindow",
  components: {ConfirmDialog},
  emits: ['back'],
  data(){
    return {
      mounts: [
        {
          target: 'D:/Example File/Example Executive File.exe',
          root: '/Example File.exe'
        },
        {
          target: 'D:/Example Folder',
          root: '/Example Folder'
        },
      ],
      ignores:[
        {
          path: 'D:/test ignore/ignore folder/ignore file.txt'
        }
      ]
    }
  },
  computed:{
    mountList(){
      let res = []
      for (const mount of this.mounts) {
        res.push({
          target: mount.target.split('').reverse().join(''),
          root: mount.root.split('').reverse().join('')
        })
      }
      return res
    },
    ignoreList(){
      let res = []
      for (const ignore of this.ignores) {
        res.push({
          path: ignore.path.split('').reverse().join('')
        })
      }
      return res
    }
  },
  methods: {
    back(){
      this.$emit('back')
    },
    remove(mount){
      this.showConfirm('Warning', 'Are you sure to remove this mount?\nThis will not delete the file/folder in the target path.')
    },
    removeIgnore(ignore){
      this.showConfirm('Warning', 'Are you sure to remove the ignore?\nThis file/folder may be mounted and visible for other users.')
    },
    edit(mount){
      window.alert('edit')
    },
    showConfirm(title = 'Warning', content = 'Are you sure to remove this item?'){
      this.$refs.confirm.show(title, content)
    }
  }
}
</script>

<style scoped>
.flex-inline{
  display: flex;
  justify-content: left;
  align-items: center;
}
.rect-btn-outlined{
  min-width: 0;
  padding: 0 4px;
}
.ellipse-rtl{
  padding-right: 16px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  direction: rtl;
  text-align: left;
  unicode-bidi: bidi-override;
}
</style>
