<template>
  <v-dialog v-model="dialog">
    <v-card :loading="loading">
      <template #loader>
        <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
      </template>
      <v-card-title style="padding-bottom: 0">Profile</v-card-title>
      <v-card-text style="padding-top: 0; padding-left: 5px; padding-right: 5px; max-height: 60vh; overflow-y: auto">
        <v-list>
          <v-list-item v-for="item in profile">
            <template #title style="">
              <v-radio-group v-if="item.radio === true" :label="item.label" :hint="item.hint" :readonly="item.readonly || loading" v-model="item.value">
                <v-radio v-for="it in item.options" :label="it" :value="it"></v-radio>
              </v-radio-group>
              <v-textarea v-else-if="item.textarea === true" :label="item.label" :hint="item.hint" :readonly="item.readonly || loading" v-model="item.value"></v-textarea>
              <v-text-field v-else :label="item.label" :hint="item.hint" v-model="item.value" :readonly="item.readonly || loading"></v-text-field>
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
export default {
  name: "ProfileDialog",
  data(){
    return {
      profile:[
        {
          label: "Name",
          hint: "Your display name.",
          value: "Wshine"
        },
        {
          label: "Email",
          hint: "Your email address.",
          value: ""
        },
        {
          radio: true,
          label: "Gender",
          options:['Male', 'Female'],
          value: "Male"
        },
        {
          'textarea': true,
          label: "Description",
          hint: "Tell others about yourself!",
          value: ""
        },
        {
          label: "Join Time",
          value: "2021-01-01 00:00:00",
          readonly: true
        }
      ],
      dialog: false,
      loading: false,
      saving: false
    }
  },
  methods:{
    save(){
      this.dialog = false
    }
  }
}
</script>

<style scoped>

</style>
