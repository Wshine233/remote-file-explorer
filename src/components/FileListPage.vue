<template>
  <ul>
    <li v-for="item in fileInfoList" :key="item.id">
      
        <div class="itemBox">
          <div class="imageBox"><img :src="item.image" class="imageShow" /></div>
          <div class="textShow">
            <span class="nameShow"> {{ item.name }}</span>
            <span class="descriptionShow"> {{ item.desc }}</span>
          </div>
        </div>
    </li>
  </ul>
</template>
<script>
// import { title } from "process";

export default {
  name: "FileListPage",

  data() {
    return {
      fileInfoList: [
        {
          id: 1001,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
        {
          id: 1002,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
        {
          id: 1003,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
        {
          id: 1004,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
        {
          id: 1005,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
        {
          id: 1006,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
        {
          id: 1007,
          image: require("@/assets/folderIcon.svg"),
          name: "我是文件的名字",
          desc: "描述",
        },
      ],
    };
  },
  methods: {
    gnerateLi() {},
  },
};
</script>

<style scoped>


.itemBox {
  width: 50%;
  height: 125px;
  margin: 0px auto;
}

.imageBox{
      width: 25%;
      display: inline-block;
}

.imageShow {
  width: 100%;
  height: 100%;
      /* width: 25%;
      display: inline-block; */

}

.textShow{
      /* float: left; */
      width: 75%;
      height: 100%;
      display: inline-block;
      text-align: left;
      bottom: 40px;
      margin-bottom: 40px;
}
.nameShow {
      height: 50%;
      font-size: large;
      background-color: blueviolet;
      display: block;
}
.descriptionShow {
      height: 50%;
      font-size: medium;
      background-color: burlywood;
      display: block;
}
li{
      list-style: none;
}
</style>
