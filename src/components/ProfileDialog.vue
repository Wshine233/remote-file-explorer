<template>
  <v-dialog v-model="dialog" :persistent="loading">
    <v-card :loading="loading">
      <template #loader>
        <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
      </template>
      <v-card-title style="padding-bottom: 0">Profile</v-card-title>
      <v-card-text style="padding-top: 0; padding-left: 5px; padding-right: 5px; max-height: 60vh; overflow-y: auto">
        <v-list>
          <v-list-item v-for="item in profile">
            <template #title style="">
              <v-radio-group v-if="item.radio === true" :label="item.label" :hint="item.hint" :readonly="item.readonly" :disabled="loading" v-model="item.value">
                <v-radio v-for="it in item.options" :label="it" :value="it"></v-radio>
              </v-radio-group>
              <v-textarea v-else-if="item.textarea === true" :label="item.label" :hint="item.hint" :readonly="item.readonly" :disabled="loading" v-model="item.value"></v-textarea>
              <v-text-field v-else :label="item.label" :hint="item.hint" v-model="item.value" :readonly="item.readonly" :disabled="loading"></v-text-field>
            </template>
          </v-list-item>
        </v-list>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="save" :disabled="loading" :loading="saving">
          Done
          <template #loader>
            <v-progress-circular size="20" width="2" indeterminate color="primary"></v-progress-circular>
          </template>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {systemState} from "@/system";
import {getTimeStr, setUserProfile} from "@/utils";

export default {
  name: "ProfileDialog",
  emits: ['update'],
  data(){
    return {
      profile:[],
      profileData: {},
      dialog: false,
      loading: false,
      saving: false
    }
  },
  methods:{
    show(data){
      this.profile = [
        {
          label: "Name",
          attr: "name",
          hint: "Your display name.",
          value: data["name"] ? data["name"] : ""
        },
        {
          label: "Email",
          attr: "email",
          hint: "Your email address.",
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
          hint: "Tell others about yourself!",
          value: data["description"] ? data["description"] : ""
        },
        {
          label: "Join Time",
          attr: "joinTime",
          value: data["joinTime"] ? getTimeStr(data["joinTime"] / 1000) : "",
          readonly: true
        }
      ]
      this.dialog = true
    },
    save(){
      this.loading = true
      let keys = ['name', 'email', 'gender', 'description']
      let values = [this.profile[0].value, this.profile[1].value, this.profile[2].value, this.profile[3].value]
      setUserProfile(keys, values).then(res => {
        this.loading = false
        this.$emit('update')
      }).catch(err => {
        this.loading = false
        window.alert(err.message)
      }).finally(() => {
        this.dialog = false
      })
    }
  }
}
</script>

<style scoped>

</style>