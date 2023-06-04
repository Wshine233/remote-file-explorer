<template>
  <v-dialog v-model="dialog">
    <v-sheet>
      <v-card :elevation="0">
        <template #title>
          <v-card-title class="header-text">Sort Method {{sort}}</v-card-title>
        </template>

        <template #text>
          <v-btn-toggle v-model="sort" class="grid-toggle" shaped mandatory>
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

      <v-divider></v-divider>

      <v-card :elevation="0">
        <template #title>
          <v-card-title class="header-text">Don't show these files</v-card-title>
        </template>

        <template #text>
          <v-chip-group
            v-model="types"
            column
            multiple
          >
            <v-chip
              filter
              variant="outlined"
            >
              Picture
            </v-chip>
            <v-chip
              filter
              variant="outlined"
            >
              Video
            </v-chip>
            <v-chip
              filter
              variant="outlined"
            >
              Audio
            </v-chip>
            <v-chip
              filter
              variant="outlined"
            >
              Text
            </v-chip>
            <v-chip
              filter
              variant="outlined"
            >
              Document
            </v-chip>
            <v-chip
              filter
              variant="outlined"
            >
              Unknown
            </v-chip>
          </v-chip-group>
        </template>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn>Done</v-btn>
        </v-card-actions>
      </v-card>
    </v-sheet>
  </v-dialog>
</template>

<script>
export default {
  name: "SortSelectDialog",
  data(){
    return {
      dialog: false,
      types: null,
      sort: null
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

.header-text{
  font-size: 18px;
  color: black;
}
</style>
