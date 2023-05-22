import {reactive} from "vue";

export const defaultState = {
    currentSession: undefined,
    globalSettings: {
        virtualMode: true, //是否开启虚拟模式（本地演示模式）
        backendUrl: "https://localhost:8080", //后端服务器地址
    }
}

let initialized = false

export let systemState = reactive(defaultState)

function initState(){
    if (localStorage.getItem("system-state") !== null){
        systemState = JSON.parse(localStorage.getItem("system-state"))
    }else{
        localStorage.setItem("system-state", JSON.stringify(defaultState))
    }
}

export function syncToLocalStorage(){
    localStorage.setItem("system-state", JSON.stringify(systemState))
    console.log("系统状态已同步到本地存储，数据明细：\n" + JSON.stringify(systemState))
}

function init(force = false){
    if (initialized && !force){
        return
    }

    initState()
    // setVirtualMode(true)

    console.log("系统初始化完毕")
}

init()

