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
              <v-btn density="comfortable" :variant="loading ? 'text' : 'outlined'" color="success" class="rect-btn-outlined" :loading="loading" @click="add">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="item in groups" :value="item.id" rounded>
                <v-list-item-title>{{item.id}}</v-list-item-title>
                <v-list-item-subtitle>{{item.permission}}</v-list-item-subtitle>
                <template #append>
                  <v-btn color="warning" variant="flat" density="comfortable" class="rect-btn" @click.stop="set(item)" :disabled="loading">
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

    <SetPermDialog ref="setPerm" @confirm="fetchGroups()"/>
  </v-window-item>

  <v-snackbar v-model="popup" timeout="2000" color="error">{{popupMsg}}</v-snackbar>
</template>

<script>
import {post} from "@/utils";
import {systemState} from "@/system";
import SetPermDialog from "@/components/SetPermDialog";

export default {
  name: "PermWindow",
  components: {SetPermDialog},
  emits: ['back'],
  data(){
    return {
      loading: false,
      groups:[],/*[
        {
          id: "admin",
          permission: "adxms"
        },
        {
          id: "user",
          permission: "-d--s"
        },
        {
          id: "restrict",
          permission: "-----"
        },
        {
          id: "guest",
          permission: "----s"
        },
      ],*/

      popup: false,
      popupMsg: "",
    }
  },
  methods: {
    popMsg(msg){
      this.popup = true
      this.popupMsg = msg
    },
    show(){
      this.fetchGroups()
    },
    back(){
      this.$emit('back')
    },
    add(){
      this.$refs.setPerm.show(true)
    },
    set(item){
      this.$refs.setPerm.show(false, item.id, item.permission)
    },
    fetchGroups(){
      this.loading = true
      post('/perm/list', {
        sessionId: systemState.currentSession
      }).then(res => {
        console.log('perm groups: ', res.data)
        this.groups = res.data
        this.loading = false
      }).catch(err => {
        this.popMsg(err.message)
        this.loading = false
      })
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
