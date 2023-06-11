<template>
  <v-slide-y-reverse-transition>
    <div v-if="visible" style="position: sticky; bottom: 0; min-height: 64px; z-index: 10086">
      <div id="player">
      </div>
      <v-btn variant="plain" color="primary" icon density="comfortable" style="position: absolute; right: 8px; top: 0; z-index: 1" @click.stop="close">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>
  </v-slide-y-reverse-transition>

</template>

<script>
import 'aplayer/dist/APlayer.min.css';
import APlayer from 'aplayer';

export default {
  name: "AudioPreviewer",
  props: ['src'],
  data(){
    return {
      visible: false,
      audio: [{
        name: '',//歌名
        artist: '',//歌手
        url: '',//音频文件地址
        cover: '',//音乐封面地址
        lrc: ""// 歌词
      }],
      ap: null
    }
  },
  methods:{
    show(title, artist){
      this.visible = true
      setTimeout(()=>{
        this.prepare(title, artist)
      }, 50)
    },
    prepare(title, artist){
      this.audio[0].name = title
      this.audio[0].artist = artist
      this.audio[0].url = this.src
      this.audio[0].cover = ''
      this.audio[0].lrc = ''

      this.ap = new APlayer({
        container: document.getElementById("player"),
        autoplay: true,
        audio: this.audio
      })
    },
    close(){
      this.visible = false
      this.ap.pause()

      setTimeout(()=>{
        this.ap.destroy()
      }, 100)
    }
  }
}
</script>

<style scoped>
  #player{
    color: black;
  }
</style>
