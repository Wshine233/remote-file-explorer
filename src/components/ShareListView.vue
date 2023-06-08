<template>
  <v-virtual-scroll id="list" item-height="60" :items="shareList">
    <template v-slot:default="{item, index}">
      <v-list-item variant="flat"
                   :title="item.name"
                   :value="item"
                   :subtitle="`${item.timeStr}${item.type === 0 ? '' : `&nbsp;&nbsp;&nbsp;&nbsp;${item.sizeStr}`}`"
                   density="comfortable"
                   height="60"
                   :class="{'user-select-disabled': true, 'item-selected': item.selected}"
                   @click="click(item)"
                   @touchstart="touchStart(item)"
                   @touchmove="touchMove"
                   @touchend="touchEnd">

        <template v-slot:prepend>
          <v-icon class="file-icon" style="margin-inline-end: 20px" :icon="getIcon(item.type, item.name)"
                  size="42"></v-icon>
        </template>

        <template v-slot:append>
          <v-btn variant="text" density="comfortable" icon="mdi-download" color="grey-lighten-1" @click.stop="clickInfo(item)"></v-btn>
        </template>

      </v-list-item>
    </template>
  </v-virtual-scroll>
</template>

<script>
export default {
  name: "ShareListView",
  props:['shareList', 'selectMode'],
  emits: ['clickDownload', 'clickItem', 'holdItem'],
  methods: {
    getIcon(type, name) {
      if (type === 0) {
        return "mdi-folder"
      } else if (name !== "") {
        return "mdi-file"
      }
    },
    click(item) {
      this.$emit('clickItem', item)
    },
    clickInfo(item){
      this.$emit('clickDownload', item)
    },
    touchStart(file) {
      this.holdTimeout = setTimeout(() => {
        this.$emit('holdItem', file)
      }, 700)
    },
    touchEnd() {
      clearTimeout(this.holdTimeout)
    },
    touchMove() {
      clearTimeout(this.holdTimeout)
    },

  }
}
</script>

<style scoped>
#list {
  /* 高度不超过屏幕底端 */
  height: calc(100vh - 112px);
}

.user-select-disabled {
  user-select: none;
}

.item-selected {
  background-color: #a0a0a0;
}

.file-icon {
  width: 40px;
  margin-inline-end: 20px;
}
</style>
