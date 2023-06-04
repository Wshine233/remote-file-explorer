<template>
  <v-window-item value="perm" class="fill-height">
    <v-card class="fill-height">
      <v-toolbar
        dark
        color="primary"
      >
        <v-btn icon dark @click="back">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title>Permission Manager</v-toolbar-title>
      </v-toolbar>
      <v-container class="overflow-y-auto" style="height: calc(100% - 64px)">
        <v-card class="flex-grow-1">
          <v-card-title>
            <div class="flex-inline">
              Perm Groups
              <v-spacer></v-spacer>
              <v-btn density="comfortable" variant="outlined" color="success" class="rect-btn-outlined">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="item in groups" :value="item.id" @click="edit(item)" rounded>
                <v-list-item-title>{{item.id}}</v-list-item-title>
                <v-list-item-subtitle>{{item.perm}}</v-list-item-subtitle>
                <template #append>
                  <v-btn color="warning" density="comfortable" variant="flat" class="rect-btn" @click.stop="set(item)">
                    <v-icon>mdi-cog</v-icon>
                  </v-btn>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        <p class="v-card-subtitle text-wrap" style="flex: auto; margin-top: 24px">To edit file's rule/visibility, select files in the main page. To edit user's permission, go to the User Manager.</p>
      </v-container>
    </v-card>
  </v-window-item>
</template>

<script>
export default {
  name: "PermWindow",
  emits: ['back'],
  data(){
    return {
      groups:[
        {
          id: "admin",
          perm: "adxms"
        },
        {
          id: "user",
          perm: "-d--s"
        },
        {
          id: "restrict",
          perm: "-----"
        },
        {
          id: "guest",
          perm: "----s"
        },
        {
          id: "test1",
          perm: "-----"
        },
        {
          id: "test2",
          perm: "-----"
        },
        {
          id: "test3",
          perm: "-----"
        },
        {
          id: "test4",
          perm: "-----"
        },
        {
          id: "test5",
          perm: "-----"
        },
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
    set(mount){
      window.alert('set')
    },
    edit(mount){
      window.alert('edit')
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
.rect-btn{
  min-width: 0;
  padding: 0 7px;
}
</style>
