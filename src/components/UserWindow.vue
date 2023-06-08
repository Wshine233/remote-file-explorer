<template>
  <v-window-item value="user" class="fill-height">
    <v-card class="fill-height">
      <v-toolbar
        dark
        color="primary"
      >
        <v-btn icon dark @click="back">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title>User Manager</v-toolbar-title>
      </v-toolbar>
      <v-container class="overflow-y-auto" style="height: calc(100% - 64px)">
        <v-card class="flex-grow-1">
          <v-card-title class="flex-inline" style="padding-bottom: 0">
            User List
            <v-spacer></v-spacer>
            <v-btn density="comfortable" variant="text" icon :loading="loading" @click="refresh">
              <v-icon>mdi-refresh</v-icon>
              <template #loader>
                <v-progress-circular size="24" width="3" indeterminate></v-progress-circular>
              </template>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-list>
              <div v-for="group in Object.keys(userList)">
                <div class="flex-inline">
                  <v-list-subheader class="font-weight-bold" style="font-size: 16px">
                    #{{group}}
                  </v-list-subheader>
                  <v-spacer></v-spacer>
                  <v-btn color="info" density="comfortable" class="rect-btn" variant="text" style="margin: 0 16px;"
                         icon @click="showBroadcast(getUsers(group), `Send to all users in group ${group}`)">
                    <v-icon>mdi-bullhorn-variant</v-icon>
                  </v-btn>
                </div>

                <v-list-item v-for="item in userList[group]" :value="item.root" @click="edit(item)" rounded>
                  <template #title>
                    <div class="flex-inline">
                      <div>
                        <v-list-item-title>{{item.id}}</v-list-item-title>
                        <v-list-item-subtitle>{{item.name}}</v-list-item-subtitle>
                      </div>
                      <v-spacer></v-spacer>
                      <div>
                        <v-btn color="info" density="comfortable" class="rect-btn" variant="text" icon>
                          <v-icon>mdi-information</v-icon>
                        </v-btn>
                        <v-btn color="important" density="comfortable" class="rect-btn" variant="text" icon>
                          <v-icon>mdi-delete-forever</v-icon>
                        </v-btn>
                      </div>
                    </div>
                  </template>
                </v-list-item>
              </div>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>

    </v-card>

    <BroadcastDialog ref="broadcast" :send-to="sendTo" :hint="sendToMsg" />
  </v-window-item>
</template>

<script>
import BroadcastDialog from "@/components/BroadcastDialog";
export default {
  name: "UserWindow",
  components: {BroadcastDialog},
  emits: ['back'],
  data(){
    return {
      loading: false,
      sendTo: [],
      sendToMsg: "",
      users:[
        {
          id: "wshine",
          name: "Wshine",
          group: "admin"
        },
        {
          id: "user1",
          name: "test account",
          group: "user"
        },
        {
          id: "user2",
          name: "test account",
          group: "user"
        },
        {
          id: "user3",
          name: "test account",
          group: "user"
        },
        {
          id: "user4",
          name: "test account",
          group: "user"
        },
        {
          id: "user5",
          name: "test account",
          group: "user"
        },
        {
          id: "user6",
          name: "test account",
          group: "user"
        },
        {
          id: "user7",
          name: "test account",
          group: "user"
        },
        {
          id: "user8",
          name: "test account",
          group: "user"
        },
        {
          id: "user9",
          name: "test account",
          group: "user"
        },
        {
          id: "user10",
          name: "test account",
          group: "user"
        },
        {
          id: "user11",
          name: "test account",
          group: "user"
        },
        {
          id: "user12",
          name: "test account",
          group: "user"
        },
        {
          id: "user13",
          name: "test account",
          group: "user"
        },
        {
          id: "user14",
          name: "test account",
          group: "user"
        },
        {
          id: "user15",
          name: "test account",
          group: "user"
        },
        {
          id: "user16",
          name: "test account",
          group: "user"
        },
        {
          id: "user17",
          name: "test account",
          group: "user"
        },
        {
          id: "user18",
          name: "test account",
          group: "user"
        },
        {
          id: "user19",
          name: "test account",
          group: "user"
        },
        {
          id: "user20",
          name: "test account",
          group: "user"
        },
        {
          id: "user21",
          name: "test account",
          group: "user"
        },
        {
          id: "user22",
          name: "test account",
          group: "user"
        }
      ],

    }
  },
  computed:{
    userList(){
      let res = {}
      for (const user of this.users) {
        if(res[user.group] === undefined){
          res[user.group] = []
        }
        res[user.group].push(user)
      }

      return res
    }
  },
  methods: {
    back(){
      this.$emit('back')
    },
    remove(mount){
      window.alert('remove')
    },
    edit(mount){
      window.alert('edit')
    },
    refresh(){
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 2000);
    },
    showBroadcast(sendTo, msg){
      this.sendTo = sendTo
      this.sendToMsg = msg
      this.$refs.broadcast.dialog = true
      console.log(sendTo)
    },
    getUsers(group){
      return this.users.filter(user => user.group === group).map(user => user.id)
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
.rect-btn{
  min-width: 0;
  padding: 0 7px;
  margin: 0 0px;
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
