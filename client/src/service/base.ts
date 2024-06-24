import { useUserStore } from '@/store'
import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// 请求拦截和响应拦截
// 添加请求拦截器
service.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    let userStore = useUserStore()
    if (userStore.token !== '') {
      config.headers.Authorization = 'Bearer ' + userStore.token
    }
    return config
  },
  function (error) {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 添加响应拦截器
service.interceptors.response.use(
  (response) => {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    return response
  },
  function (error) {
    // 超出 2xx 范围的状态码都会触发该函数。
    // 对响应错误做点什么
    if (!error.response) {
      console.error('无法连接服务器')
      return Promise.reject(error)
    }
    console.log('error' + error.response.status)
    switch (error.response.status) {
      case 401:
        console.error('请重新登录')
        break
      case 404:
        console.error('当前路径有误')
        break
      case 500:
        console.error('服务器连接失败 请稍后再试')
        break
      default:
        console.error('未知错误')
        break
    }
    return Promise.reject(error)
  }
)

export default service
