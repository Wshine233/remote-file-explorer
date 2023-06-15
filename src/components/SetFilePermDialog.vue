<template>
  <v-dialog v-model="dialog" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        <span class="headline">Set File Permission</span>
      </v-card-title>
      <v-card-text style="max-height: 60vh; overflow-y: auto">
        <v-form ref="form">
          <v-text-field v-model="fileInfo.file" label="File" required readonly
                        hint="Absolute Path in server's machine." :loading="loadingFile" :disabled="loadingFile"/>
          <v-select v-model="fileInfo.visibleGroup" :items="groupItems" label="Visible Group" multiple closable-chips
                    required
                    hint="Groups that can see this file." :loading="loadingPerm" :disabled="loadingPerm"/>
          <v-select v-model="fileInfo.visibleUser" :items="userItems" label="Visible User" multiple closable-chips
                    required
                    hint="Users that can see this file." :loading="loadingPerm" :disabled="loadingPerm"/>
          <v-select v-model="fileInfo.invisibleUser" :items="userItems" label="Invisible User" multiple closable-chips
                    required
                    hint="Users that cannot see this file." :loading="loadingPerm" :disabled="loadingPerm"/>

          <v-table fixed-header style="margin-bottom: 10px">
            <thead>
            <tr>
              <th class="text-left">
                Target
              </th>
              <th class="text-left">
                Action
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="rule in fileInfo.rules">
              <td>
                {{ `${rule.type === 0 ? '#' : '@'}${rule.target}: ${rule.permission}` }}
              </td>
              <td>
                <v-btn color="important" icon @click="removeRule(rule)" density="comfortable" variant="text">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
            </tbody>
          </v-table>
          <v-btn @click="showPermEdit">Create rule</v-btn>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="dialog = false" :disabled="loading">Cancel</v-btn>
        <v-btn color="info" @click="confirmEdit" :loading="loading">Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="editPermDialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">Edit Permission</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-select v-model="newRule.type" :items="[0, 1]" label="Type" @update:modelValue="onUpdateType"/>
          <v-select v-model="newRule.target" :items="newRule.type === 0 ? groupItems : userItems" label="Target" @update:modelValue="onUpdateTarget"/>
          <v-text-field v-model="newRule.permission" label="Permission" required/>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="info" @click="addRule(newRule)">Confirm</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <ConfirmDialog ref="confirm"/>

  <v-snackbar v-model="popup" :timeout="2000" :color="success ? 'success' : 'error'">
    {{ errMsg }}
    <template #actions>
      <v-btn @click="popup = false">Close</v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import {checkSuperUser, post} from "@/utils";
import {systemState} from "@/system";
import ConfirmDialog from "@/components/ConfirmDialog";

export default {
  name: "SetFilePermDialog",
  emits: ['confirm'],
  components: {ConfirmDialog},
  data() {
    return {
      dialog: false,
      editPermDialog: false,
      loadingFile: false,
      loadingPerm: false,
      loadingUser: false,

      file: {},
      fileInfo: {
        file: "D:/test",
        visibleGroup: [],
        visibleUser: [],
        invisibleUser: [],
        rules: [
          {
            type: 0,  //0为组，1为用户
            target: 'admin',
            permission: '*****'
          }
        ]
      },
      groups: [],
      users: [],
      headers: [
        {text: 'Type', value: 'type'},
        {text: 'Target', value: 'target'},
        {text: 'Permission', value: 'permission'},
      ],
      newRule: {
        type: 0,
        target: "admin",
        permission: "*****"
      },

      popup: false,
      errMsg: '',
      success: false,

    }
  },
  computed: {
    groupItems() {
      return this.groups
    },
    userItems() {
      return this.users
    },
    loading(){
      return this.loadingFile || this.loadingPerm || this.loadingUser
    }
  },
  methods: {
    popMsg(msg, success = false) {
      this.popup = true;
      this.errMsg = msg;
      this.success = success;
    },
    removeRule(rule) {
      this.$refs.confirm.show('Warning', 'Are you sure to remove this rule?', false, () => {
        this.fileInfo.rules.splice(this.fileInfo.rules.indexOf(rule), 1)
      })
    },
    addRule(rule){
      for (let i = 0; i < this.fileInfo.rules.length; i++) {
        if (this.fileInfo.rules[i].type === rule.type && this.fileInfo.rules[i].target === rule.target) {
          this.fileInfo.rules[i].permission = rule.permission
          this.editPermDialog = false
          return
        }
      }

      this.fileInfo.rules.push(rule)
      this.editPermDialog = false
    },
    onUpdateType(){
      if(this.newRule.type === 0){
        this.newRule.target = this.groups[0]
      }else{
        this.newRule.target = this.users[0]
      }
    },
    onUpdateTarget(){
      for (const rule of this.fileInfo.rules) {
        if(rule.type === this.newRule.type && rule.target === this.newRule.target){
          this.newRule.permission = rule.permission
          return
        }
      }
      this.newRule.permission = '*****'
    },
    confirmEdit(){
      this.loadingFile = true
      this.loadingPerm = true
      this.loadingUser = true

      post('/file/set-rule', {
        sessionId: systemState.currentSession,
        path: this.file.path,
        rule: this.fileInfo
      }).then(res => {
        this.popMsg('Edit successfully.', true)
        this.dialog = false
        this.$emit('confirm')
      }).catch(err => {
        this.popMsg(err.message)
      }).finally(() => {
        this.loadingFile = false
        this.loadingPerm = false
        this.loadingUser = false
      })
    },
    show(file) {
      //如果没有权限（非super user）则不能进入此界面
      this.dialog = true
      this.loadingFile = true
      this.loadingPerm = true
      this.loadingUser = true
      this.file = file

      checkSuperUser().then(res => {
        this.fetchInfo()
      }).catch(err => {
        this.popMsg("You don't have permission to set file permission.")
        this.dialog = false
      })
    },
    fetchInfo() {
      this.loadingFile = true
      this.loadingPerm = true
      this.loadingUser = true

      post('/file/rule', {
        sessionId: systemState.currentSession,
        path: this.file.path
      }).then(res => {
        console.log('file perm info: ', res.data)
        this.fileInfo = res.data
        this.loadingFile = false
      }).catch(err => {
        this.popMsg(err.message)
        this.loadingFile = false
        this.dialog = false
      })

      post('/user/list', {
        sessionId: systemState.currentSession,
        keys: ['id']
      }).then(res => {
        this.users = res.data.map(item => item.id)
        this.loadingUser = false
      }).catch(err => {
        this.popMsg(err.message)
        this.loadingUser = false
        this.dialog = false
      })

      post('/perm/list', {
        sessionId: systemState.currentSession
      }).then(res => {
        console.log('perm groups: ', res.data.map(group => group.id))
        this.groups = res.data.map(group => group.id)
        this.loadingPerm = false
      }).catch(err => {
        this.popMsg(err.message)
        this.loadingPerm = false
        this.dialog = false
      })

    },
    showPermEdit() {
      this.editPermDialog = true
      this.onUpdateType()
      this.onUpdateTarget()
    },
  }
}
</script>

<style scoped>

</style>
