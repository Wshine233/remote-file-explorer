<template>
  <v-dialog v-model="dialog">
    <v-sheet>
      <v-card :elevation="0">

        <v-card-title class="header-text">Sort Method</v-card-title>

        <v-card-text style="padding-bottom: 0">
          <v-list-subheader>{{ sortMethods[sort] ? sortMethods[sort].name : "" }}</v-list-subheader>
          <v-btn-toggle v-model="sort" color="primary" shaped mandatory>
            <v-btn v-for="sort in sortMethods" variant="outlined">
              <v-icon size="x-large">{{ sort.icon }}</v-icon>
            </v-btn>
          </v-btn-toggle>

          <v-switch v-model="descending" :label="descending ? 'Descending' : 'Ascending'" hide-details></v-switch>
        </v-card-text>

      </v-card>

      <v-divider></v-divider>

      <v-card :elevation="0">
        <template #title>
          <v-card-title class="header-text">Don't show these files</v-card-title>
        </template>

        <template #text>
          <v-chip-group v-model="types" column multiple>
            <v-chip filter variant="outlined" value="folder" filter-icon="mdi-close">
              Folder
            </v-chip>
            <v-chip filter variant="outlined" value="picture" filter-icon="mdi-close">
              Picture
            </v-chip>
            <v-chip filter variant="outlined" value="video" filter-icon="mdi-close">
              Video
            </v-chip>
            <v-chip filter variant="outlined" value="audio" filter-icon="mdi-close">
              Audio
            </v-chip>
            <v-chip filter variant="outlined" value="text" filter-icon="mdi-close">
              Text
            </v-chip>
            <v-chip filter variant="outlined" value="document" filter-icon="mdi-close">
              Document
            </v-chip>
            <v-chip filter variant="outlined" value="archive" filter-icon="mdi-close">
              Archive
            </v-chip>
            <v-chip filter variant="outlined" value="unknown" filter-icon="mdi-close">
              Unknown
            </v-chip>
          </v-chip-group>
        </template>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="confirm">Done</v-btn>
        </v-card-actions>
      </v-card>
    </v-sheet>
  </v-dialog>
</template>

<script>
import {sortByFileName, sortByRandom, sortBySize, sortByTime} from "@/utils";

export default {
  name: "SortSelectDialog",
  emits: ['confirm'],
  data() {
    return {
      dialog: false,
      types: [],
      sort: 0,
      descending: false,
      sortMethods: [
        {
          name: "File Name",
          icon: "mdi-sort-alphabetical-ascending",
          method: sortByFileName
        },
        {
          name: "File Size",
          icon: "mdi-sort-numeric-ascending",
          method: sortBySize
        },
        {
          name: "File Time",
          icon: "mdi-sort-clock-ascending",
          method: sortByTime
        },
        {
          name: "Random",
          icon: "mdi-dice-5",
          method: sortByRandom
        }
      ]
    }
  },
  methods: {
    show() {
      this.dialog = true;
    },
    confirm(){
      let result = {
        sort: this.sortMethods[this.sort].method,
        descending: this.descending,
        blockTypes: this.types
      }
      this.$emit('confirm', result);
      this.dialog = false;
    }
  }
}
</script>

<style scoped>
.grid-toggle {
  position: relative;
  height: auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}

.grid-toggle > * {
  padding: 10px;
}

.header-text {
  font-size: 18px;
  padding-bottom: 0;
}
</style>
