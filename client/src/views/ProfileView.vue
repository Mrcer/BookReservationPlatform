<script setup lang="ts">

</script>

<template>
  <div class="main">
    <div class="container">
      <div>
        <el-avatar :size="120" />
        <span class="user-name">User</span>
      </div>
      <el-divider />
      <div>
        <el-row :span="8">
          <el-menu default-active="1">
            <el-menu-item index="1">
              General
            </el-menu-item>
          </el-menu>
        </el-row>
        <el-row :span="16">
          <RouterView />
        </el-row>
      </div>
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
