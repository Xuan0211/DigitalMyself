import {Service} from './service'
export function sendMsg(data) {
  return Service({
    url: '/manager/sendMsg',
    data: JSON.stringify(data)
  })
}

export function getList() {
  return Service({
    url: '/manager/getFileList',
    method: 'get'
  })
}

export function changeFileState(id, state){
  return Service({
    url: '/manager/changeFileState',
    method: 'get',
    params: {
      id,
      state
    }
  })
}
