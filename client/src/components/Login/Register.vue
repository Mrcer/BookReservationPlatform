<script setup lang="ts">
import { ref } from 'vue'
import {createUser} from '../../service/user'
import { ElMessageBox } from 'element-plus'

const registerForm = ref({
  username:'', 
  password:'', 
  email:'', 
  role:'',
})

const message = ref('')

const handleRegister = () => {

  createUser(registerForm)
  .then((res)=>{
    if(res.data.status === 201){
      message.value = res.data.value.message
    }
    else if(res.data.status === 400){
      message.value = res.data.value.error
    }
    else{
      console.log("Unknown status code")
    }
  })
  .catch((err)=>{console.log(err)})

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
