<template>
  <v-dialog v-model="dialog" transition="slide-y-reverse-transition">
    <v-card>
      <v-card-title style="padding-bottom: 3px">Send Message</v-card-title>

      <v-card-text>
        <v-text-field v-model="msgTitle" label="Title" variant="outlined"></v-text-field>
        <v-textarea v-model="msg" label="Message" variant="outlined" hide-details></v-textarea>
        <div style="display: flex">
          <v-checkbox v-model="anonymous" label="Anonymous" hide-details style="position: relative; left: -11px"></v-checkbox>
          <v-checkbox v-model="important" label="Important" hide-details style="position: relative; left: -11px"></v-checkbox>
        </div>
        <div v-if="noSendTo || hint" class="important-text">{{ hint ? hint : 'Broadcast' }}</div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="send" :disabled="loading" :loading="loading">Send</v-btn>
      </v-card-actions>

    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "BroadcastDialog",
  props: ['sendTo', 'hint'],
  data() {
    return {
      dialog: false,
      msgTitle: "",
      msg: "",
      anonymous: false,
      loading: false,
      important: false
    }
  },
  computed:{
    noSendTo(){
      return this.sendTo === undefined || this.sendTo === null || this.sendTo.length <= 0
    }
  },
  methods: {
    send() {
      this.loading = true
    }
  }
}
</script>

<style scoped>

.important-text{
  color: red;
  font-weight: bold;
}

</style>
