<script setup lang="ts">
import { ref } from 'vue'

import { useUserStore } from '../../store/index'
import { ElMessageBox } from 'element-plus'

const userStore = useUserStore()

const message = ref('')


const loginForm = ref({
  username: '',
  password: '',
})


const handleLogin = async () => {
  let res = await userStore
    .login(loginForm.value.username, loginForm.value.password)
    .then(() => '登录成功')
    .catch((err) => '登录失败，请检查用户名或密码')
  message.value = res
  ElMessageBox.alert(message.value, '提示', {
    // if you want to disable its autofocus
    // autofocus: false,
    confirmButtonText: 'OK',
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
