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
                  <v-btn v-if="labMode" color="info" density="comfortable" class="rect-btn" variant="text" style="margin: 0 16px;"
                         icon @click="showBroadcast(getUsers(group), `Send to all users in group ${group}`)">
                    <v-icon>mdi-bullhorn-variant</v-icon>
                  </v-btn>
                </div>

                <v-list-item v-for="item in userList[group]" :value="item.root" rounded>
                  <template #title>
                    <div class="flex-inline">
                      <div>
                        <v-list-item-title>{{item.id}}</v-list-item-title>
                        <v-list-item-subtitle>{{item.name}}</v-list-item-subtitle>
                      </div>
                      <v-spacer></v-spacer>
                      <div>
                        <v-btn color="info" density="comfortable" class="rect-btn" variant="text" icon :disabled="loading" @click.stop="edit(item)">
                          <v-icon>mdi-information</v-icon>
                        </v-btn>
                        <v-btn color="important" density="comfortable" class="rect-btn" variant="text" icon :disabled="loading" @click.stop="remove(item)">
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
    <ProfileDialog ref="profile" @update="fetchUsers"/>
  </v-window-item>

  <ConfirmDialog ref="confirm"/>
  <v-snackbar v-model="popup" color="error" timeout="3000">{{popupMsg}}</v-snackbar>
</template>

<script>
import BroadcastDialog from "@/components/BroadcastDialog";
import {getTimeStr, listUsers, post, setUserProfile} from "@/utils";
import {lab, systemState} from "@/system";
import ProfileDialog from "@/components/ProfileDialog";
import ConfirmDialog from "@/components/ConfirmDialog";
export default {
  name: "UserWindow",
  components: {ConfirmDialog, ProfileDialog, BroadcastDialog},
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
          permissionGroup: "admin"
        },
        {
          id: "user1",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user2",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user3",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user4",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user5",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user6",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user7",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user8",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user9",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user10",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user11",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user12",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user13",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user14",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user15",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user16",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user17",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user18",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user19",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user20",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user21",
          name: "test account",
          permissionGroup: "user"
        },
        {
          id: "user22",
          name: "test account",
          permissionGroup: "user"
        }
      ],
      groups: ["admin", "user"],

      popup: false,
      popupMsg: "",
    }
  },
  computed:{
    userList(){
      let res = {}
      for (const user of this.users) {
        if(res[user.permissionGroup] === undefined){
          res[user.permissionGroup] = []
        }
        res[user.permissionGroup].push(user)
      }

      return res
    },
    labMode(){
      return lab
    }
  },
  methods: {
    show(){
      this.fetchUsers()
    },
    popMsg(msg){
      this.popup = true
      this.popupMsg = msg
    },
    back(){
      this.$emit('back')
    },
    remove(item){
      this.$refs.confirm.show("Warning", "Are you sure to REMOVE this user?\nYou cannot revert this action!!!!!", true, res => {
        if(!res) return
        post("/user/remove", {
          sessionId: systemState.currentSession,
          userId: item.id
        }).then(res => {
          this.fetchUsers()
        }).catch(err => {
          this.popMsg(err.message)
        })
      })
    },
    edit(data){
      let profile = [
        {
          label: "ID",
          attr: "id",
          hint: "User unique ID.",
          value: data["id"] ? data["id"] : "",
          readonly: true
        },
        {
          label: "Name",
          attr: "name",
          hint: "User display name.",
          value: data["name"] ? data["name"] : ""
        },
        {
          'select': true,
          items: this.groups,
          label: "Group",
          attr: "permissionGroup",
          hint: "User permission group.",
          value: data["permissionGroup"] ? data["permissionGroup"] : ""
        },
        {
          label: "Permission",
          attr: "permission",
          hint: "User override permission.",
          value: data["permission"] ? data["permission"] : "*****"
        },
        {
          label: "Email",
          attr: "email",
          hint: "User email address.",
          value: data["email"] ? data["email"] : ""
        },
        {
          radio: true,
          label: "Gender",
          attr: "gender",
          options:['Male', 'Female'],
          value: data["gender"] ? data["gender"] : "Male"
        },
        {
          'textarea': true,
          label: "Description",
          attr: "description",
          hint: "User's description.",
          value: data["description"] ? data["description"] : ""
        },
        {
          label: "Join Time",
          attr: "joinTime",
          value: data["joinTime"] ? getTimeStr(data["joinTime"] / 1000) : "",
          readonly: true
        }
      ]
      this.$refs.profile.showCustom(profile, this.saveMethod)
    },
    saveMethod(profile){
      return post('/user/set-info', {
        sessionId: systemState.currentSession,
        keys: [
          profile[1].attr,
          profile[2].attr,
          profile[3].attr,
          profile[4].attr,
          profile[5].attr,
          profile[6].attr,
        ],
        values: [
          profile[1].value,
          profile[2].value,
          profile[3].value,
          profile[4].value,
          profile[5].value,
          profile[6].value,
        ],
        userId: profile[0].value
      })
    },
    refresh(){
      this.fetchUsers()
    },
    showBroadcast(sendTo, msg){
      this.sendTo = sendTo
      this.sendToMsg = msg
      this.$refs.broadcast.dialog = true
      console.log(sendTo)
    },
    getUsers(group){
      return this.users.filter(user => user.permissionGroup === group).map(user => user.id)
    },
    fetchUsers(){
      this.loading = true
      listUsers().then(users => {
        this.users = users
      }).catch(err => {
        this.popMsg(err.message)
      }).finally(() => {
        this.loading = false
      })

      post('/perm/list', {
        sessionId: systemState.currentSession
      }).then(res => {
        this.groups = res.data.map(group => group.id)
      }).catch(err => {
        this.popMsg(err.message)
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
