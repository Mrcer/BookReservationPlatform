<script setup lang="ts">
import { useUserStore } from '@/store';
import { RouterView } from 'vue-router';

const user = useUserStore();

</script>

<template>
  <div class="main">
    <div class="container">
      <div>
        <span class="user-name">{{ user.username }}</span>
      </div>
      <el-divider />
      <el-row>
        <el-col :span="4">
          <el-menu default-active="1" router>
            <el-menu-item index="/profile/general">个人信息</el-menu-item>
            <el-menu-item index="/profile/reservations">我的预约</el-menu-item>
            <el-menu-item index="/profile/borrowed">我的借阅</el-menu-item>
          </el-menu>
        </el-col>
        <el-col :span="20">
          <RouterView />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 4rem;
}

.container {
  width: 80%;
  max-width: 800px;
}

.user-name {
  margin-left: 1rem;
  font-size: 4rem;
  font-weight: bold;
}
</style>
