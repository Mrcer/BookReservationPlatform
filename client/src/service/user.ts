import service from './base'
import { userUrl } from './api'
import type { UserInfo, UserRole } from '@/types'
import { useUserStore } from '@/store'

export interface dbUser {
  user_id: number
  username: string
  password: string
  email: string
  points: number
  registration_date: string
  role: UserRole
}

// 注册用户
const register = (username: string, password: string, email: string, role: UserRole) => {
  return service
    .post<{
      message: string
      userId: number
    }>(userUrl.register, {
      username,
      password,
      email,
      role,
    })
    .catch((error) => {
      console.log(error)
      throw error.response.status as number
    })
}

// 用户登录
const login = async (username: string, password: string) => {
  let req = service.post<{
    token: string
    userId: number
    role: UserRole
  }>(userUrl.login, { username, password })
  let serverData = (await req).data
  return serverData
}

// 查看用户信息
const getUserInfo = async (userId: number) => {
  let req = service.get<{
    userId: number
    username: string
    email: string
    points: number
    registration_date: string
    role: UserRole
  }>(userUrl.info(userId))
  let serverData = (await req).data
  let result: UserInfo = {
    id: serverData.userId,
    username: serverData.username,
    email: serverData.email,
    credit: serverData.points,
    registration_date: serverData.registration_date,
    role: serverData.role,
  }
  return result
}

// 查看用户积分
const getUserCredit = async (userId: number): Promise<number> => {
  let req = service.get(userUrl.info(userId)) as any
  let serverData = (await req).data
  return serverData.points
}

// 修改个人信息
const updateUserInfo = (email: string) => {
  let userStore = useUserStore()
  service.put(userUrl.updateInfo(userStore.uid), { email })
}

// 更改用户积分
const updateUserCredit = (userId: number, credit: number) => {
  service.put(userUrl.updateCredit(userId), { points: credit })
}

// 新增用户
const addUser = (data: dbUser) => {
  return service.post(userUrl.add, data)
}

// 删除用户
const deleteUser = (userId: number) => {
  return service.delete(userUrl.delete(userId))
}

export {
  register,
  login,
  getUserInfo,
  getUserCredit,
  updateUserInfo,
  updateUserCredit,
  addUser,
  deleteUser,
}

