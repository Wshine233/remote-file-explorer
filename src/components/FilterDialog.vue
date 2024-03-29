<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>Filter</v-card-title>
      <v-card-text class="card-text">
        <v-expansion-panels v-model="filters" multiple>
          <v-expansion-panel value="folder">
            <v-expansion-panel-title class="font-weight-bold" expand-icon="mdi-filter-variant-plus"
                                     collapse-icon="mdi-close">Folder
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-text-field v-model="searchDir"
                            :label="`Filter Dir`"
                            :hint="`Folder you want to search.`"
                            placeholder="e.g.  /test/folder"
                            variant="underlined"></v-text-field>
              <v-switch v-model="searchDirRecursive" label="Recursive" density="compact"></v-switch>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-expansion-panel value="type">
            <v-expansion-panel-title class="font-weight-bold" expand-icon="mdi-filter-variant-plus"
                                     collapse-icon="mdi-close">Types
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="flex">
                <v-checkbox class="flex-inline" v-model="searchTypeFolder" label="Folder"
                            density="compact"></v-checkbox>
                <v-checkbox class="flex-inline" v-model="searchTypeFile" label="File" density="compact"></v-checkbox>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-slide-y-transition>
            <v-expansion-panel value="extension" v-if="ext">
              <v-expansion-panel-title class="font-weight-bold" expand-icon="mdi-filter-variant-plus"
                                       collapse-icon="mdi-close">Extensions
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div>
                  <v-text-field v-model="searchExtension"
                                :label="`Filter Extension (${searchExtensionInvert ? 'black list' : 'white list'})`"
                                :hint="`Extensions you ${searchExtensionInvert ? 'DON\'T' : ''} want to search. (Divide with ';')`"
                                placeholder="e.g.  txt;mp3;ogg"
                                variant="underlined"></v-text-field>
                  <v-switch v-model="searchExtensionInvert" label="Use Black List" density="compact"></v-switch>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-slide-y-transition>


          <v-expansion-panel value="modified">
            <v-expansion-panel-title class="font-weight-bold" expand-icon="mdi-filter-variant-plus"
                                     collapse-icon="mdi-close">Modified Time
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="flex">
                <div class="flex flex-column">
                  <v-list-item-title class="flex-grow-1 flex-text">From</v-list-item-title>
                  <v-list-item-title class="flex-grow-1 flex-text">To</v-list-item-title>
                </div>
                <div class="flex flex-column">
                  <v-btn variant="text" style="margin-left: 10px"
                         @click="showDateTimePicker(this.searchModifiedTimeRange[0], this.searchModifiedTimeRange, 0)">{{modifiedFrom}}
                  </v-btn>
                  <v-btn variant="text" style="margin-left: 10px"
                         @click="showDateTimePicker(this.searchModifiedTimeRange[1], this.searchModifiedTimeRange, 1)">{{modifiedTo}}
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-expansion-panel value="created">
            <v-expansion-panel-title class="font-weight-bold" expand-icon="mdi-filter-variant-plus"
                                     collapse-icon="mdi-close">Create Time
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="flex">
                <div class="flex flex-column">
                  <v-list-item-title class="flex-grow-1 flex-text">From</v-list-item-title>
                  <v-list-item-title class="flex-grow-1 flex-text">To</v-list-item-title>
                </div>
                <div class="flex flex-column">
                  <v-btn variant="text" style="margin-left: 10px"
                         @click="showDateTimePicker(this.searchCreateTimeRange[0], this.searchCreateTimeRange, 0)">{{createdFrom}}
                  </v-btn>
                  <v-btn variant="text" style="margin-left: 10px"
                         @click="showDateTimePicker(this.searchCreateTimeRange[1], this.searchCreateTimeRange, 1)">{{createdTo}}
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>

      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <DateTimePicker ref="date" @input="updateDateTime"/>
</template>

<script>
import DateTimePicker from "@/components/DateTimePicker";
import {getDateTimeStr} from "@/utils";

export default {
  name: "FilterDialog",
  emits: ['save'],
  components: {DateTimePicker},
  data() {
    return {
      dialog: false,
      filters: [],
      searchDir: '',  // 在以下目录搜索，多个目录用分号分隔（'D:/asdasd; C:/asdaSd'） 当前在哪个目录就会默认添加一个该目录的过滤器
      searchDirRecursive: false,  // 在以下目录搜索，是保留还是排除
      searchExtension: '', // 文件扩展名（'txt;mp4;mp3;rar'）
      searchExtensionInvert: false, //文件扩展名是保留还是排除
      searchTypeFolder: true, //checkbox，搜索文件类型，是文件夹还是文件
      searchTypeFile: true, //checkbox，搜索文件类型，是文件夹还是文件
      searchModifiedTimeRange: [new Date(),new Date()], //搜索修改时间范围
      searchCreateTimeRange: [new Date(), new Date()],   //搜索创建时间范围

      pickVal: null,
      pickIndex: null
    }
  },
  computed:{
    ext(){
      if(this.filters.find(f => f === 'type') && !this.searchTypeFile){
        return false
      }
      return true
    },
    modifiedFrom(){
      return this.getDisplayTimeStr(this.searchModifiedTimeRange[0])
    },
    modifiedTo(){
      return this.getDisplayTimeStr(this.searchModifiedTimeRange[1])
    },
    createdFrom(){
      return getDateTimeStr(this.searchCreateTimeRange[0])
    },
    createdTo(){
      return getDateTimeStr(this.searchCreateTimeRange[1])
    }
  },
  methods: {
    show(filter){
      this.filters = []
      this.dialog = true

      setTimeout(() => {
        if(filter.folder !== undefined){
          this.filters.push('folder')
          this.searchDir = filter.folder
          this.searchDirRecursive = filter.recursive
        }
        if(filter.type !== undefined){
          this.filters.push('type')
          this.searchTypeFolder = filter.type.includes(0)
          this.searchTypeFile = filter.type.includes(1)
        }
        if(filter.ext !== undefined){
          this.filters.push('extension')
          this.searchExtension = filter.ext
          this.searchExtensionInvert = filter.ext_blacklist
        }
        if(filter.time_modified !== undefined){
          this.filters.push('modified')
          this.searchModifiedTimeRange = filter.time_modified
        }
        if(filter.time_created !== undefined){
          this.filters.push('created')
          this.searchCreateTimeRange = filter.time_created
        }
      }, 100)
    },
    save() {
      this.dialog = false
      this.$emit('save', this.getFilter())
    },
    getFilter(){
      let filter = {}

      if(this.filters.includes('folder')){
        filter.folder = this.searchDir
        filter.recursive = this.searchDirRecursive
      }
      if(this.filters.includes('type')){
        let type = []
        if(this.searchTypeFolder){
          type.push(0)
        }
        if(this.searchTypeFile){
          type.push(1)
        }
        filter.type = type
      }
      if(this.filters.includes('extension') && (!filter.type || filter.type.includes(1))){
        filter.ext = this.searchExtension
        filter.ext_blacklist = this.searchExtensionInvert
      }
      if(this.filters.includes('modified')){
        filter.time_modified = this.searchModifiedTimeRange
      }
      if(this.filters.includes('created')){
        filter.time_created = this.searchCreateTimeRange
      }

      return filter
    },
    getDisplayTimeStr(d){
      if(isNaN(d.getTime())){
        d = new Date()
        return getDateTimeStr(d)
      }
      return getDateTimeStr(d)
    },
    showDateTimePicker(date, pickVal, pickIndex){
      this.$refs.date.dialog = true
      this.$refs.date.setDateTime(date)

      this.pickVal = pickVal
      this.pickIndex = pickIndex
    },
    updateDateTime(d){
      this.pickVal[this.pickIndex] = d
      //如果开始时间大于结束时间，就交换
      if(this.pickVal[0].getTime() > this.pickVal[1].getTime()) {
        let temp = this.pickVal[0]
        this.pickVal[0] = this.pickVal[1]
        this.pickVal[1] = temp
      }
    }
  }
}
</script>

<style scoped>
.flex {
  display: flex;
  flex-wrap: nowrap;
}

.flex-column {
  flex-direction: column;
}

.flex-text {
  text-align: left;
  padding: 6px 0;
}

.card-text {
  max-height: 60vh;
  overflow-y: auto;
}
</style>
