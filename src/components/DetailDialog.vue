<template>
  <v-dialog transition="dialog-bottom-transition"
            width="auto"
            v-model="dialog">
    <v-card>
      <v-card-text>
        {{dialogInfo.text}}
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DetailDialog",
  props: ['fileInfo'],
  data(){
    return {
      dialog: false,
      dialogInfo: {
        text: "这是放置详细信息的界面"
      },
    }
  },

}
</script>

<style scoped>

</style>
