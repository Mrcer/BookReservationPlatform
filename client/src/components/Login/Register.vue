<script setup lang="ts">
import { ref } from 'vue'
import { register } from '../../service/user'
import { ElMessageBox } from 'element-plus'
import { UserRole } from '@/types'

const registerForm = ref({
  username: '',
  password: '',
  email: '',
})

const message = ref('')

const handleRegister = () => {
  let form = registerForm.value
  register(form.username, form.password, form.email, UserRole.Student)
    .then((res) => {
      if (res.data.status === 201) {
        message.value = res.data.value.message
      } else if (res.data.status === 400) {
        message.value = res.data.value.error
      } else {
        console.log('Unknown status code')
      }
    })
    .catch((err) => {
      console.log(err)
    })

  ElMessageBox.alert(message.value, 'notion', {
    // if you want to disable its autofocus
    // autofocus: false,
    confirmButtonText: 'OK',
  })
}
</script>

<template>
  <div>
    <el-form :model="registerForm" label-width="100px">
      <el-form-item label="username">
        <el-input v-model="registerForm.username" placeholder="Please enter your username" />
      </el-form-item>
      <el-form-item label="email">
        <el-input v-model="registerForm.email" placeholder="Please enter your email" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input
          v-model="registerForm.password"
          type="password"
          placeholder="Please enter your password"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">Create</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped></style>
