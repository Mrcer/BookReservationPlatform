<script setup lang="ts">
import { ref } from 'vue'

const registerForm = ref({
  net_id: '',
  name: '',
  password: '',
})

const handleRegister = () => {
  console.log(registerForm.value)
}
</script>

<template>
  <div>
    <el-form :model="registerForm" label-width="100px">
      <el-form-item label="NetID">
        <el-input v-model="registerForm.net_id" placeholder="Please enter your NetID" />
      </el-form-item>
      <el-form-item label="Name">
        <el-input v-model="registerForm.name" placeholder="Please enter your name" />
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
