<template>
  <v-dialog v-model="dialog">
    <v-img ref="img" :class="{'rotated': rotate, 'normal': !rotate}" :src="src" contain @click="rotateImg">
      <template #placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>
      </template>
      <template #error>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-icon color="error" size="64" style="width: 100%; height: 100%" @click.stop="dialog = false">mdi-image-broken</v-icon>
        </v-row>
      </template>
    </v-img>
  </v-dialog>
</template>

<script>
export default {
  name: "ImagePreviewDialog",
  props: ['src'],
  data(){
    return {
      dialog: false,
      rotate: false
    }
  },
  methods: {
    show(){
      this.dialog = true;
      this.rotate = false;
    },
    rotateImg(){
      this.rotate = !this.rotate;
    }
  }
}
</script>

<style scoped>
.normal{
  position: fixed;
  transform: translate(-50%, -50%);
  left: calc(50vw - 24px);
  width: 80vw;
  height: 80vh;
  max-width: 80vw;
  max-height: 80vh;

  background-color: rgba(0, 0, 0, 0.16);
}
.rotated{
  position: fixed;
  transform: rotate(90deg) translate(-50%, -50%);
  transform-origin: top left;
  left: calc(50vw - 24px);
  top: 0vh;
  max-width: 80vh;
  max-height: 80vw;
  width: 80vh;
  height: 80vw;

  background-color: rgba(0, 0, 0, 0.16);
}
</style>
