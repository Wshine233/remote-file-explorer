<template>
  <v-dialog v-model="dialog" fullscreen transition="slide-y-reverse-transition">
    <v-card color="surface">
      <v-card-title class="no-padding card-title-sticky">
        <v-sheet class="sheet-title" color="surface">
          <v-btn icon variant="text" style="margin-right: 10px" @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          User History
        </v-sheet>
      </v-card-title>
      <v-timeline side="end" style="padding-right: 24px">
        <v-timeline-item v-for="item in history" :key="item.timeStr" :dot-color="item.type" size="small">
          <v-alert :value="true" :color="item.type" :icon="item.icon" density="compact" style="font-size: 14px">
            <v-alert-title style="font-size: 18px">{{ item.timeStr }}</v-alert-title>
            <v-alert-title style="font-size: 16px">{{ item.action }}</v-alert-title>
            {{ item.message }}
          </v-alert>
        </v-timeline-item>
      </v-timeline>
    </v-card>
  </v-dialog>

</template>

<script>
export default {
  name: "HistoryDialog",
  props: ['sessionId'],
  data() {
    return {
      dialog: false,
      history: [
        {
          id: 0,
          type: 'important',
          icon: 'mdi-delete-forever',
          timeStr: "2021-01-01 00:08:00",
          action: "Delete",
          userId: "wshine",
          message: "Delete file: /Example Folder/Example File/Long Name File Example to Test Overflow.png"
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
        {
          id: 1,
          type: 'success',
          icon: 'mdi-login',
          timeStr: "2021-01-01 00:00:00",
          action: "Login",
          userId: 'wshine',
          message: "Successfully login."
        },
      ]
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
