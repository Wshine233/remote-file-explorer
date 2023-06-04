<template>
  <v-dialog v-model="dialog">
    <v-sheet>
      <v-card>
        <template #title>
          <v-card-title class="font-weight-bold">选择视图</v-card-title>
        </template>

        <template #text>
          <v-btn-toggle class="grid-toggle" shaped mandatory>
            <v-btn>
              <v-icon>mdi-format-align-left</v-icon>
            </v-btn>

            <v-btn>
              <v-icon>mdi-format-align-center</v-icon>
            </v-btn>

            <v-btn>
              <v-icon>mdi-format-align-right</v-icon>
            </v-btn>

            <v-btn>
              <v-icon>mdi-format-align-justify</v-icon>
            </v-btn>

            <v-btn>
              <v-icon>mdi-format-align-justify</v-icon>
            </v-btn>

            <v-btn>
              <v-icon>mdi-format-align-justify</v-icon>
            </v-btn>

            <v-btn>
              <v-icon>mdi-format-align-justify</v-icon>
            </v-btn>
          </v-btn-toggle>
        </template>
      </v-card>
    </v-sheet>
  </v-dialog>
</template>

<script>
export default {
  name: "ViewSelectDialog",
  data(){
    return {
      dialog: false,
    }
  },
}
</script>

<style scoped>
.grid-toggle{
  position: relative;
  height: auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}

.grid-toggle > * {
  padding: 10px;
}
</style>
