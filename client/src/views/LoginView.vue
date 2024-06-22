<script setup lang="ts">
import Login from '@/components/Login/Login.vue'
import Register from '@/components/Login/Register.vue'
import { useUserStore } from '@/store'
import { ref } from 'vue'

const userStore = useUserStore()
const showLogin = ref(true)
</script>

<template>
  <div class="main">
    <div class="wapper">
      <el-menu
        class="menu"
        default-active="1"
        mode="horizontal"
        @select="
          (index: string) => {
            showLogin = index === '1'
          }
        "
      >
        <el-menu-item index="1">登录</el-menu-item>
        <el-menu-item index="2">注册</el-menu-item>
      </el-menu>
      <Login v-if="showLogin" />
      <Register v-else />
    </div>
  </div>
</template>

<style scoped>
.main {
  display: flex;
  justify-content: center;
  height: 100vh;
}

.wapper {
  width: 800px;
  height: auto;
  border: 2px solid #ccc;
  border-radius: 20px;
  margin-top: 2rem;
  padding: 1rem;
}

.menu {
  margin-bottom: 2rem;
}
</style>
