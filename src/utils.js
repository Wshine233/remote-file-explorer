
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
