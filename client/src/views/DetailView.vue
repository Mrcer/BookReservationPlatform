<script setup lang="ts">
import { useRoute } from 'vue-router'
import CommentInput from '@/components/Detail/CommentInput.vue'
import CommentList from '@/components/Detail/CommentList.vue'
const route = useRoute()
</script>

<template>
  <div>
    <h1>书籍详情页</h1>
    <p>当前书籍的id是：{{ route.params.id }}</p>
    <CommentInput />
    <CommentList />
  </div>
</template>

<style scoped></style>
