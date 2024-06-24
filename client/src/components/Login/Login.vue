<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '../../store/index'

const userStore = useUserStore()

const loginForm = ref({
  username: '',
  password: '',
})

const handleLogin = () => {
  let res = userStore.login(loginForm.value.username, loginForm.value.password)
  res.catch((err) => {
    alert('登录失败')
  })
}
</script>

<template>
  <div>
    <el-form :model="loginForm" label-width="100px">
      <el-form-item label="Username">
        <el-input v-model="loginForm.username" placeholder="Please enter your username" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="Please enter your password"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">Login</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped></style>
