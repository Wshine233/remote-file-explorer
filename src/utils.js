import axios from "axios";
import {systemState, clipBoard, syncToLocalStorage} from "@/system";
import {hashPassword, requestGetUserInfo, requestUpdateUserInfo, requestUpdateUserPassword} from "@/user-manager";


export function getTimeStr(time){
  console.log(`time: ${time}`)
  if(time === null){
    return "unknown"
  }
  time = new Date(parseInt((time * 1000).toString()))
  return getDateTimeStr(time)
}

export function getDateTimeStr(time){
  if(time === null){
    return "unknown"
  }
  const year = time.getFullYear().toString().padStart(4, '0');
  const month = (time.getMonth() + 1).toString().padStart(2, '0');
  const day = time.getDate().toString().padStart(2, '0');
  const hour = time.getHours().toString().padStart(2, '0');
  const minute = time.getMinutes().toString().padStart(2, '0');
  const second = time.getSeconds().toString().padStart(2, '0');
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}

export function getDateStr(time){
  if(time === null){
    return "unknown"
  }
  time = new Date(parseInt((time * 1000).toString()))
  const year = time.getFullYear().toString().padStart(4, '0');
  const month = (time.getMonth() + 1).toString().padStart(2, '0');
  const day = time.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`
}

export function getReadableSize(size){
  if(size === null){
    return "unknown"
  }
  if(size < 1024){
    return `${size}B`
  }else if(size < 1024 * 1024){
    return `${(size / 1024).toFixed(2)}KB`
  }else if(size < 1024 * 1024 * 1024){
    return `${(size / 1024 / 1024).toFixed(2)}MB`
  }else{
    return `${(size / 1024 / 1024 / 1024).toFixed(2)}GB`
  }
}

export function sortByFileName(fileList){
  //按文件名排序，优先显示文件夹
  fileList.sort((a, b) => {
    if(a.type === 0 && b.type !== 0){
      return -1
    }else if(a.type !== 0 && b.type === 0){
      return 1
    }else{
      return a.name.localeCompare(b.name)
    }
  })

  return fileList
}

export function sortByTime(fileList){
  //按时间排序，优先显示文件夹; 若时间相同，按文件名排序
  fileList.sort((a, b) => {
    if (a.type === 0 && b.type !== 0) {
      return -1
    } else if (a.type !== 0 && b.type === 0) {
      return 1
    } else {
      if (a.time === b.time) {
        return a.name.localeCompare(b.name)
      } else {
        return a.time - b.time
      }
    }
  })

  return fileList
}

export function sortBySize(fileList){
  //按文件大小排序，优先显示文件夹; 若大小相同，按文件名排序
  fileList.sort((a, b) => {
    if (a.type === 0 && b.type !== 0) {
      return -1
    } else if (a.type !== 0 && b.type === 0) {
      return 1
    } else {
      if (a.size === b.size) {
        return a.name.localeCompare(b.name)
      } else {
        return a.size - b.size
      }
    }
  })

  return fileList
}

export function sortByRandom(fileList){
  //随机排序，但优先显示文件夹
  fileList.sort((a, b) => {
    if (a.type === 0 && b.type !== 0) {
      return -1
    } else if (a.type !== 0 && b.type === 0) {
      return 1
    } else {
      return Math.random() - 0.5
    }
  })

  return fileList
}

export function sortShareList(shares){
  //按时间排序，优先显示未过期的
  shares.sort((a, b) => {
    let aExpired = a.expired * 1000 < Date.now()
    let bExpired = b.expired * 1000 < Date.now()
    if(aExpired && !bExpired){
      return 1
    }
    if(!aExpired && bExpired){
      return -1
    }
    return b.time - a.time
  })

  return shares
}

export function getFileExtType(ext, type = 1) {
  if(type === 0){
    return 'folder'
  }
  if(ext.length === 0){
    return 'unknown'
  }
  if(ext[0] === '.'){
    if(ext.length === 1){
      return 'unknown'
    }
    ext = ext.substring(1)
  }
  ext = ext.toLowerCase()

  if(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(ext)){
    return 'picture'
  }

  if(['mp4', 'rmvb', 'webm', 'flv', 'avi', 'mov', 'wmv', 'mkv'].includes(ext)){
    return 'video'
  }

  if(['mp3', 'wav', 'ogg', 'flac', 'aac', 'ape', 'wma'].includes(ext)){
    return 'audio'
  }

  if(['txt', 'cfg', 'log', 'json', 'md', 'lrc', 'ass'].includes(ext)){
    return 'text'
  }

  if(['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf'].includes(ext)){
    return 'document'
  }

  if(['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz'].includes(ext)){
    return 'archive'
  }

  return "unknown"
}

export function getFileIcon(type, name) {
  if (type === 0) {
    return "mdi-folder"
  }
  if (name.indexOf('.') === -1) {
    return "mdi-file"
  }
  let suffix = name.split('.').pop().toLowerCase()
  let extType = getFileExtType(suffix)
  switch (extType) {
    case 'picture':
      return "mdi-image"
    case 'video':
      return "mdi-video"
    case 'audio':
      return "mdi-music-box"
    case 'text':
      return "mdi-text-box"
    case 'document':
      return "mdi-file-document"
    case 'archive':
      return "mdi-zip-box"
  }

  return "mdi-file"
}

export function parseUrlParams(url){
  let params = {}
  if(url.indexOf('?') === -1){
    return params
  }

  let paramStr = url.split('?')[1]
  if(paramStr){
    let paramArr = paramStr.split('&')
    for(let i = 0; i < paramArr.length; i++){
      let param = paramArr[i].split('=')
      if (param.length !== 2) {
        continue
      }
      params[param[0]] = param[1]
    }
  }
  return params
}

export function getFileName(path){
  let arr = path.split('/')
  return arr[arr.length - 1]
}

export function getFileExtension(path){
  if(path.lastIndexOf('.') === -1){
    return ''
  }else{
    return path.substring(path.lastIndexOf('.'))
  }
}

export function getFileStem(path){
  let name = getFileName(path)
  if(name.lastIndexOf('.') === -1){
    return name
  }else{
    return name.substring(0, name.lastIndexOf('.'))
  }
}

export function post(url, data){
  axios.defaults.baseURL = systemState.globalSettings.backendUrl
  return new Promise((resolve, reject) => {
    axios.post(url, data).then(res => {
      let data = res.data
      if(data.success){
        resolve(data)
      }else {
        reject(data)
      }
    }).catch(err => {
      reject(err.data ? err.data : err)
    })
  })
}


export function checkSuperUser(){
  return new Promise((resolve, reject) => {
    post('/user/super', {
      sessionId: systemState.currentSession
    }).then(res => {
      if(res.data){
        resolve(res)
      }else{
        reject(res)
      }
    }).catch(err => {
      reject(err)
    })
  })
}


export function getUserGroup(){
  let request = requestGetUserInfo(systemState.currentSession, ['permissionGroup'])
  return new Promise((resolve, reject) => {
    request.then(res => {
      if(res.success){
        resolve(res.data.permissionGroup)
      }else{
        reject(res)
      }
    })
  })
}


export function getUserProfile(){
  let request = requestGetUserInfo(systemState.currentSession, ['name', 'email', 'gender', 'description', 'joinTime', 'permissionGroup', 'permission'])
  return new Promise((resolve, reject) => {
    request.then(res => {
      if(res.success){
        resolve(res.data)
      }else{
        reject(res)
      }
    })
  })
}


export function setUserProfile(keys, values){
  let request = requestUpdateUserInfo(systemState.currentSession, keys, values)
  return new Promise((resolve, reject) => {
    request.then(res => {
      if(res.success){
        resolve(res)
      }else{
        reject(res)
      }
    })
  })
}


export function listUsers(){
  let request = post('/user/list', {
    sessionId: systemState.currentSession,
    keys: ['id', 'name', 'email', 'gender', 'description', 'joinTime', 'permissionGroup', 'permission']
  })

  return new Promise((resolve, reject) => {
    request.then(res => {
      resolve(res.data)
    }).catch(err => {
      reject(err)
    })
  })
}


export function updatePassword(oldPassword, newPassword){
  let oldHash = hashPassword(oldPassword)
  let newHash = hashPassword(newPassword)

  let request = requestUpdateUserPassword(systemState.currentSession, oldHash, newHash)
  return new Promise((resolve, reject) => {
    request.then(res => {
      if(res.success){
        resolve(res)
      }else{
        reject(res)
      }
    })
  })
}


export function isParentPath(pathParent, pathChild){
  if(pathParent === pathChild){
    return true
  }
  if(pathParent[pathParent.length - 1] !== '/'){
    //保证不出现以下情况的误判：'/a/bc'.startsWith('/a/b')
    pathParent += '/'
  }
  return pathChild.startsWith(pathParent)
}


//转接因复制后路径改变的文件路径
export function getNewPath(oldPath, oldParent, newParent){
  // /a/b/c/d   /a/b -> /aa/b   /a/b/c/d -> /aa/b/c/d
  if(oldPath === oldParent){
    let fileName = getFileName(oldParent)
    if(newParent[newParent.length - 1] !== '/'){
      newParent += '/'
    }
    return newParent + fileName
  }
  let fileName = getFileName(oldParent)
  if(newParent[newParent.length - 1] !== '/'){
    newParent += '/'
  }
  newParent += fileName + '/'
  let newPath = newParent + oldPath.substring(oldParent.length)
  return newPath
}


export function updateClipboard(result, newParent){
  let validResult = []
  for (const item of result) {
    //先把所有失败了且要删除的项目从剪贴板删除
    if(!item.success && item.cancel){
      delete clipBoard[item.path]
    }else{
      validResult.push(item)
    }
  }

  //将结果按路径深度从深到浅排序
  validResult.sort((a, b) => {
    return b.path.split('/').length - a.path.split('/').length
  })

  //将剪贴板中的项目路径更新
  for (const item of validResult) {
    if(item.success){
      //为什么复制模式也要更新路径？考虑以下情况：/a/b复制到/d，/a/b/c复制到/d，/a移动到/d，如果第一个和第三个成功了，则/a/b/c的位置依然发生了改变
      //先delete掉自己，防止被重复判断
      if(item.cancel){
        delete clipBoard[item.path]
      }
      for (const path of Object.keys(clipBoard)){
        if(isParentPath(item.path, path)){
          let newPath = getNewPath(path, item.path, newParent)
          clipBoard[newPath] = clipBoard[path]
          delete clipBoard[path]
        }
      }
    }
  }

  syncToLocalStorage()
}


export function joinPath(parent, child){
  if(parent[parent.length - 1] === '/'){
    return parent + child
  }else{
    return parent + '/' + child
  }
}


export function requestPasteItem(pathFrom, parentTo){
  //pathFrom must be a list

  return new Promise((resolve, reject) => {
    let files = []
    for (const path of pathFrom) {
      if(clipBoard[path] === undefined){
        reject({
          success: false,
          message: 'Item not found.'
        })
        return
      }
      files.push({
        path: path,
        mode: clipBoard[path].mode
      })
    }

    post('/file/copy-move', {
      sessionId: systemState.currentSession,
      files: files,
      newParent: parentTo
    }).then(res => {
      //获取结果列表
      let result = res.data
      updateClipboard(result, parentTo)
      resolve(result)
    }).catch(err => {
      reject(err)
    })
  })
}


export function addToClipboard(path, type, mode){
  clipBoard[path] = {
    type: type,
    mode: mode,
    time: Date.now()
  }
}


export function removeFromClipboard(path){
  delete clipBoard[path]
}
