import {Service} from './service'
export function sendMsg(data) {
  return Service({
    url: '/manager/sendMsg',
    data: JSON.stringify(data)
  })
}
