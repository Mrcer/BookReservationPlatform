<script setup lang="ts">
import BookManage from '@/components/Admin/BookManage.vue'
import UserManage from '@/components/Admin/UserManage.vue'
import ActivityManage from '@/components/Admin/ActivityManage.vue'
import { useUserStore } from '@/store'
import { UserRole } from '@/types'

const user = useUserStore()
</script>

<template>
  <div class="main">
    <h1 v-if="user.role !== UserRole.Admin">You are not authorized to access this page.</h1>
    <div style="width: 60%" v-else>
      <UserManage class="manage-component" />
      <BookManage class="manage-component" />
      <ActivityManage class="manage-component" />
    </div>
  </div>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
}

.manage-component {
  margin-top: 1rem;
  width: 100%;
  height: 50vh;
}
</style>
