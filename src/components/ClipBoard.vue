<template>
  <v-slide-y-reverse-transition>
    <v-btn v-if="visible" class="float-btn" icon color="success" size="large" @click="drawer = !drawer">
      <v-icon>mdi-clipboard-multiple-outline</v-icon>
    </v-btn>
  </v-slide-y-reverse-transition>

  <v-layout>
    <v-navigation-drawer v-model="drawer" location="right">
      <v-list style="height: calc(100% - 85px)">
        <v-container v-for="item in list" style="padding-bottom: 0">
          <v-card elevation="1">
            <v-card-subtitle style="padding-top: 12px">
              <v-badge dot :color="item.mode === 'move' ? 'important' : '#00000000'" style="margin-right: 8px">
                <v-icon>{{item.icon}}</v-icon>
              </v-badge>
              {{item.name}}
            </v-card-subtitle>
            <v-card-actions>
              <v-btn color="important" @click="remove(item)">Remove</v-btn>
              <v-btn color="info" @click="paste(item)">Paste</v-btn>
            </v-card-actions>
          </v-card>
        </v-container>
      </v-list>
      <v-container style="position: sticky; bottom: 0">
        <v-card>
          <v-card-actions>
            <v-btn color="important" @click="clearAll">Clear All</v-btn>
            <v-btn color="info" @click="pasteAll">Paste All</v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-navigation-drawer>
  </v-layout>
</template>

<script>
import {clipBoard} from "@/system";
import {getFileIcon, getFileName} from "@/utils";

export default {
  name: "ClipBoard",
  props: ['path'],
  data(){
    return {
      drawer: false,
    }
  },
  computed: {
    visible(){
      return clipBoard !== undefined && Object.keys(clipBoard).length > 0
    },
    list(){
      let result = []
      for(let key of Object.keys(clipBoard)){
        result.push({
          path: key,
          name: getFileName(key),
          icon: getFileIcon(clipBoard[key].type, key),
          mode: clipBoard[key].mode
        })
      }
      return result
    }
  },
  methods: {
    clearAll(){
      for (let key of Object.keys(clipBoard)) {
        delete clipBoard[key]
      }
    },
    pasteAll(){

    },
    remove(item){
      delete clipBoard[item.path]
    },
    paste(item){

    }
  }
}
</script>

<style scoped>
.float-btn{
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translate(-50%, -50%);

  z-index: 100;
}

</style>
