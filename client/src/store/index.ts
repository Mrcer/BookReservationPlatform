import type { UserRole } from '@/types'
import { defineStore } from 'pinia'

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
  actions: {},
})
