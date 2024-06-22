import { defineStore } from 'pinia'

export const useUserStore = defineStore('User', {
  state: () => ({
    isLoggedIn: false,
    uid: '',
    username: '',
  }),
  getters: {},
  actions: {},
})
