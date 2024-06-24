<script setup lang="ts">
import { useUserStore } from '@/store'
import { UserRole } from '@/types'
import { useRouter } from 'vue-router'

const router = useRouter()

const userStore = useUserStore()
</script>

<template>
  <el-header class="tittle-bar">
    <el-row class="tittle-warper">
      <RouterLink to="/">
        <el-icon class="go-back-icon">
          <HomeFilled />
        </el-icon>
      </RouterLink>
      <el-menu class="menu" mode="horizontal" router text-color="#fff" active-text-color="#fff">
        <el-menu-item index="reserve" v-if="userStore.isLoggedIn">预约板块</el-menu-item>
        <el-menu-item index="profile" v-if="userStore.isLoggedIn">用户主页</el-menu-item>
        <!-- TODO: admin auth -->
        <el-menu-item index="admin" v-if="false">管理页面</el-menu-item>
      </el-menu>
      <div class="user-info" v-if="userStore.isLoggedIn">
        <span>{{ userStore.username }}</span>
      </div>
      <div class="user-info" v-else>
        <el-button type="primary" @click="router.push('/login')" round>登录</el-button>
      </div>
    </el-row>
  </el-header>
</template>

<style scoped>
.tittle-bar {
  height: 80px;
  background-color: #005826;
}

.tittle-warper {
  display: flex;
  height: 100%;
  margin: auto 320px;
  align-items: center;
}

.go-back-icon {
  font-size: 3rem;
  background-color: #fff;
  color: #005826;
  border-radius: 50%;
  padding: 10px;
  margin-right: 20px;
}

.menu {
  min-width: 60%;
  background-color: #005826;
}

.user-info {
  color: #fff;
  margin-left: auto;
  font-size: 1.2rem;
}

@media (max-width: 1080px) {
  .tittle-warper {
    margin: auto 10px;
  }
}
</style>
