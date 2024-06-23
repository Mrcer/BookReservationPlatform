import service from './base'
import {userUrl} from './api'

// 注册用户
const createUser = (data: any) => {
  return service.post(userUrl.register, data)
}

// 用户登录
const userLogin = (data: any, userStore: any) => {
  service.post(userUrl.login, data)
  .then((res)=>{
    if(res.data.status === 200){
      userStore.isLoggedIn = true
      userStore.uid = res.data.value.userId
      userStore.username = data.username
    }
    else if(res.data.status === 400){
        alert(res.data.error)
    }
  })
  .catch((err)=>{
    console.log(err)
  })
}

export {createUser, userLogin}