<template>
  <v-dialog v-model="dialog" fullscreen transition="slide-y-reverse-transition">
    <v-card color="surface">
      <v-card-title class="no-padding card-title-sticky">
        <v-sheet class="sheet-title" color="surface">
          <v-btn icon variant="text" style="margin-right: 10px" @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          Sharing
        </v-sheet>
      </v-card-title>
      <v-expansion-panels>
        <v-expansion-panel v-for="item in shareList">
          <v-expansion-panel-title>
            <div style="display: flex; flex-direction: column; align-items: flex-start">
              {{item.time}}
              <v-list-item-subtitle style="margin-top: 8px">{{item.paths.length}} file(s)</v-list-item-subtitle>
            </div>
            <template #actions>
              <v-icon v-if="item.outdated">mdi-timer-remove-outline</v-icon>
            </template>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <p :class="{'expired-text': item.outdated, 'normal-text': !item.outdated}" style="margin-bottom: 10px">Expire Time: {{item.expired}}</p>
            <p class="raw-list" v-for="path in item.paths">
              {{path}}
            </p>
          </v-expansion-panel-text>
          <v-expansion-panel-text>
            <v-btn v-if="!item.outdated" variant="outlined">Copy share link and password</v-btn>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-dialog>
</template>

<script>
import {getTimeStr, sortShareList} from "@/utils";

export default {
  name: "SharingDialog",
  data(){
    return {
      dialog: false,
      shares: [
        {
          time: 1000,
          expired: 2000,
          paths: ['/Example Folder/Overflow/test/Start/Try/GO/EXE.EXE', '/Example File']
        },
        {
          time: 1000,
          expired: 5000000000,
          paths: ['/Example Folder', '/Example File']
        },
        {
          time: 3000,
          expired: 8000,
          paths: ['/Example Folder', '/Example File']
        },
        {
          time: 1000,
          expired: 2000,
          paths: ['/Example Folder', '/Example File']
        },
        {
          time: 1000,
          expired: 2000,
          paths: ['/Example Folder', '/Example File']
        },
        {
          time: 1000,
          expired: 2000,
          paths: ['/Example Folder', '/Example File']
        },
        {
          time: 1000,
          expired: 2000,
          paths: ['/Example Folder', '/Example File']
        },
        {
          time: 1000,
          expired: 2000,
          paths: ['/Example Folder', '/Example File']
        },
      ]
    }
  },
  computed: {
    shareList(){
      let res = []
      for (const share of this.shares) {
        console.log(share.expired, Date.now())
        res.push({
          time: getTimeStr(share.time),
          expired: getTimeStr(share.expired),
          outdated: share.expired * 1000 < Date.now(),
          pathStr: share.paths.join(', \n'),
          paths: share.paths
        })
      }
      return res
    }
  },
  methods:{
    getShareList(){
      this.shares = sortShareList(this.shares)
    }
  },
  watch: {
    dialog(val){
      if (val) {
        this.getShareList()
      }
    }
  }
}
</script>

<style scoped>
  .expired-text{
    color: red;
  }
  .normal-text{
    color: #1890ff;
  }
  .raw-list{
    margin: 6px 0;
  }
</style>
