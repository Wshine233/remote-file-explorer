<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title class="headline">Group Upgrade Request</v-card-title>
      <v-card-text>
        <v-select v-model="requestGroup" :items="availableGroups" label="Request Group"></v-select>
        <v-textarea v-model="reason" label="Reason" max-rows="5"></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" @click="dialog = false">
          Send
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "GroupUpgradeRequestDialog",
  data() {
    return {
      dialog: false,
      availableGroups: [],
      requestGroup: "",
      reason: ""
    }
  },
  methods: {
    send() {

    }
  }
}
</script>

<style scoped>

</style>
