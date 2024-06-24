import type { UserRole } from '@/types'
import { defineStore } from 'pinia'
import { login as loginApi, getUserInfo as getUserInfoApi } from '@/service/user'
export const useUserStore = defineStore('User', {
  state: () => ({
    isLoggedIn: false,
    uid: 0,
    username: '',
    email: '',
    credit: 0,
    role: '' as UserRole,
    registrationDate: '',
    token: '',
  }),
  getters: {},
  actions: {
    async login(username: string, password: string) {
      let loginRes = await loginApi(username, password)
      this.uid = loginRes.userId
      this.username = username
      this.role = loginRes.role
      this.token = loginRes.token
      let infoRes = await getUserInfoApi(this.uid)
      this.email = infoRes.email
      this.credit = infoRes.credit
      this.registrationDate = infoRes.registration_date
    }
  },
})
