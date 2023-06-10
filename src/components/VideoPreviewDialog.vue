<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>
        <span class="headline">Video Preview</span>
      </v-card-title>
      <v-card-text>
        <div id="video-player">
          <vue3-video-player :src="src"></vue3-video-player>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "VideoPreviewDialog",
  props: ['src'],
  data(){
    return{
      dialog: false,
      video: null,
      error: false
    }
  },
  methods: {
    show(title = 'Video Preview'){
      this.dialog = true
      this.prepare(title)
    },
    prepare(title){

    }
  }
}
</script>

<style scoped>

</style>
