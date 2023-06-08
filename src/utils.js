
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

  if(['mp4', 'rmvb', 'webm', 'ogg', 'flv', 'avi', 'mov', 'wmv', 'mkv'].includes(ext)){
    return 'video'
  }

  if(['mp3', 'wav', 'ogg', 'flac', 'aac', 'ape', 'wma'].includes(ext)){
    return 'audio'
  }

  if(['txt'].includes(ext)){
    return 'text'
  }

  if(['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'md'].includes(ext)){
    return 'document'
  }

  if(['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz'].includes(ext)){
    return 'archive'
  }

  return "unknown"

}
