<script setup lang="ts">
import { useUserStore } from '@/store';

const user = useUserStore();

</script>

<template>
  <div class="warpper">
    <h3>id: {{ user.uid }}</h3>
    <h3>用户名：{{ user.username }}</h3>
    <h3>邮箱：{{ user.email }}</h3>
    <h3>积分：{{ user.credit }}</h3>
    <h3>注册时间：{{ user.registrationDate }}</h3>
  </div>
</template>

<style scoped>

.warpper {
  padding: 20px;
}

</style>
