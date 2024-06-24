import Mock from 'mockjs'
import { userUrl } from '@/service/api'
import { UserRole } from '@/types'

export const registerResult = Mock.mock(import.meta.env.VITE_API_URL + userUrl.register, 'post', {
  value: {
    message: 'User registered successfully',
    userId: 123,
  },
  status: 201,
})

export const loginResult = Mock.mock(import.meta.env.VITE_API_URL + userUrl.login, 'post', {
  value: {
    token: 'jwt_token',
    userId: 123,
    role: 'student',
  },
  status: 200,
})

export const getUserInfo = Mock.mock(import.meta.env.VITE_API_URL + userUrl.info(1), 'get', {
  userId: 1,
  username: "Tim",
  email: "tim@example.com",
  points: 10,
  registration_data: "2077-01-01T00:00:00.000Z",
  role: UserRole.Student  
})