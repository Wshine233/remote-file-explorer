<template id="body">
  <div class="list-unit" v-for="file in fileList" :key="file.name">
    <div class="bg" :style="{backgroundImage: `url(${getIcon(file.type, file.name)})`}"></div>
    <div class="info-container">
      <div class="info-title clickable" @click="click(file)">{{file.name}}</div>
      <div class="info-detail">
        <div class="info-time">{{file.time}}</div>
        <div class="info-perm">{{file.perm}}</div>
      </div>
    </div>
    <button type="button" class="btn-menu"></button>
    <div class="overlay" @click="click(file)"></div>
  </div>
</template>

<script>
import axios from "axios";

const folderImg = new URL("../assets/folderIcon.svg", import.meta.url).href
const logoImg = new URL("../assets/logo.png", import.meta.url).href

export default {
  name: "FileList",
  data(){
    return{
      fileList: [
        {
          name: "Example Folder",
          type: 0,
          time: "2021-01-01 00:00:00",
          perm: "adxms"
        },
        {
          name: "Example File",
          type: 1,
          time: "2021-01-01 00:00:00",
          perm: "ad-ms"
        }
      ]
    }
  },
  methods:{
    getIcon(type, name){
      if(type === 0){
        return folderImg
      }else if(name !== ""){
        return logoImg
      }
    },
    click(file){
      window.alert(`你点击了: ${file.name}`)
    },
    getFileList(){
      axios.defaults.baseURL = "http://127.0.0.1:8512"
      axios.post('/file/list-file', {
        sessionId: "f6adf99f-f32c-417a-ae0f-bb97e6a05bc6",
        path: "/临时工作间",
      }).then(res => {
        console.log(res)
        res = res.data
        let list = []
        if(res.success){
          for(let file of res.data){
            list.push({
              name: file.path.substr(file.path.lastIndexOf('/') + 1),
              type: file.type,
              time: "2021-01-01 00:00:00",
              perm: "adxms"
            })
          }
          this.fileList = list
        }else{
          window.alert(res.message)
        }
      })
    }
  },
  created() {
    this.getFileList()
  }

}
</script>

<style scoped>
  #body{
    width: 100%;
    height: 100%;
  }

  .list-unit{
    position: relative;
    width: 100%;
    height: 100px;

    display: flex;
    flex-direction: row;
    /*justify-content: space-between;*/
    align-items: center;

    padding: 20px;
    box-sizing: border-box;

    background-color: aliceblue;
  }

  .bg{
    width: 60px;
    height: 60px;
    background-repeat: no-repeat;
    background-size: contain;
    flex-grow: 0;
    flex-shrink: 0;

    margin-right: 20px;
  }

  .info-container{
    width: calc(100% - 60px - 20px - 20px - 30px);

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    height: calc(100% - 10px);
  }

  .info-title{
    font-size: 20px;
    font-weight: bold;
    user-select: none;
    flex-shrink: 1;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .info-detail{
    display: flex;
    flex-direction: row;

    color: gray;
    font-size: 14px;
  }

  .info-perm{
    margin-left: 10px;
  }

  .btn-menu{
    margin-left: 20px;
    width: 30px;
    height: 30px;
    flex-shrink: 0;
    position: absolute;
    right: 0;
    margin-right: 20px;

    background-image: url('@/assets/more.svg');
    background-repeat: no-repeat;
    background-size: contain;
    border: none;
    background-color: transparent;

    transition: filter 0.2s;
    z-index: 1;
  }

  .btn-menu:hover{
    cursor: pointer;
    filter: brightness(1.3);
  }

  .btn-menu:active{
    filter: brightness(0.8);
  }

  .clickable{
    transition: color 0.2s;
  }

  .clickable:hover{
    color: #1890ff;
    cursor: pointer;
  }

  .overlay{
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;

    cursor: pointer;

    transition: all 0.2s;
  }

  .overlay:hover{
    background-color: rgba(0,0,0,0.1);
  }

  .overlay:active{
    background-color: rgba(0,0,0,0.2);
  }

  .btn-menu:hover + .overlay{
    background-color: rgba(0,0,0,0.1);
  }


</style>
