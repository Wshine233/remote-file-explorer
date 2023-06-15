import {reactive} from "vue";

export const defaultState = {
  currentSession: undefined,
  globalSettings: {
    virtualMode: true, //是否开启虚拟模式（本地演示模式）
    backendUrl: "http://localhost:8512", //后端服务器地址
  }
}

let initialized = false

export let systemState = reactive(defaultState)
export let clipBoard = reactive({
  '/Example Folder/Example File': {
    type: 1,
    mode: 'copy',
    time: 1023
  },
  '/Example Folder/Example Folder 2': {
    type: 0,
    mode: 'move',
    time: 1024
  }
})
export let lab = true

function initState() {
  if (localStorage.getItem("system-state") !== null) {
    systemState = JSON.parse(localStorage.getItem("system-state"))
  } else {
    localStorage.setItem("system-state", JSON.stringify(defaultState))
  }
  systemState.globalSettings.virtualMode = false
  // systemState.globalSettings.backendUrl = "http://192.168.0.135:8512"

  if (localStorage.getItem("clip-board") !== null) {
    clipBoard = JSON.parse(localStorage.getItem("clip-board"))
  } else {
    clipBoard = {}
  }
}

export function syncToLocalStorage() {
  localStorage.setItem("system-state", JSON.stringify(systemState))
  console.log("系统状态已同步到本地存储，数据明细：\n" + JSON.stringify(systemState))

  localStorage.setItem("clip-board", JSON.stringify(clipBoard))
  console.log("剪贴板已同步到本地存储，数据明细：\n" + JSON.stringify(clipBoard))
}

function init(force = false) {
  if (initialized && !force) {
    return
  }

  initState()
  // setVirtualMode(true)

  console.log("系统初始化完毕")
}

init()

