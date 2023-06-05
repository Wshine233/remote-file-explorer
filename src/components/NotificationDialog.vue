<template>
  <v-dialog v-model="dialog" fullscreen transition="slide-y-reverse-transition">
    <v-card color="surface">
      <v-card-title class="no-padding card-title-sticky">
        <v-sheet class="sheet-title" color="surface">
          <v-btn icon variant="text" style="margin-right: 10px" @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          Notifications
        </v-sheet>
      </v-card-title>
      <v-sheet style="padding: 10px">
        <v-expansion-panels>
          <v-expansion-panel v-for="item in note">
            <v-expansion-panel-title :color="item.read ? 'surface' : 'warning'" disable-icon-rotate>
              <div>
                <v-list-item-title>{{item.title}}</v-list-item-title>
                <v-list-item-subtitle>{{item.time}}</v-list-item-subtitle>
              </div>
              <template v-slot:actions>
                <v-icon v-if="!item.read || item.type === 'important'" icon="mdi-alert-circle"/>
              </template>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-list-item-subtitle style="margin-bottom: 10px; margin-top: 10px">From: {{item.sender}}</v-list-item-subtitle>
              <div>{{item.message}}</div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-sheet>
    </v-card>
  </v-dialog>

</template>

<script>
export default {
  name: "NotificationDialog",
  props: ['sessionId'],
  data() {
    return {
      dialog: false,
      note: [
        {
          title: "Test1",
          time: "2021-01-01 00:00:00",
          type: "info",
          sender: "admin1",
          read: false,
          message: "This is a test message."
        },
        {
          title: "Test important",
          time: "2021-01-01 00:00:00",
          type: "important",
          sender: "admin2",
          read: true,
          message: "This is an IMPORTANT test message."
        },
        {
          title: "Test2",
          time: "2021-01-01 00:00:00",
          type: "info",
          sender: "admin3",
          read: true,
          message: "This is an read message. And it's not important."
        }
      ]
    }
  },
  methods:{
    getIcon(type, state){
      if(type === 'info'){
        return state === 0 ?  'mdi-chevron-down' : 'mdi-chevron-up'
      }else if(type === 'important'){
        return 'mdi-information'
      }
    }
  }
}
</script>

<style scoped>
.no-padding{
  padding: 0
}
.card-title-sticky{
  position: sticky;
  top: 0;
  z-index: 2;
}
.sheet-title{
  display: flex;
  align-items: center;
  padding: 8px 16px
}
</style>
