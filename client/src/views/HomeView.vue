<script setup lang="ts">
import Search from '@/components/Home/Search.vue'
import BookBrowser from '@/components/Home/BookBrowser.vue'
</script>

<template>
  <div>
    <h1>Slogon</h1>
    <Search />
    <h2>推荐活动啥的，在搜索后隐藏</h2>
    <!-- 设计要求在这里嵌入的预约组件可能需要附着在某个按钮上，点击按钮后弹出预约组件 -->
    <BookBrowser />
  </div>
</template>

<style scoped></style>
