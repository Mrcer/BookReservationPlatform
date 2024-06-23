<script setup lang="ts">
import { useRoute } from 'vue-router'
import CommentInput from '@/components/Detail/CommentInput.vue'
import CommentList from '@/components/Detail/CommentList.vue'
import Detail from '@/components/Detail/Detail.vue'
const route = useRoute()
</script>

<template>
  <div>
    <h1>书籍详情页</h1>
    <p>当前书籍的id是：{{ route.params.id }}</p>
    <Detail :book_id="parseInt(route.params.id[0])"/>
    <CommentInput :book_id="parseInt(route.params.id[0])"/>
    <CommentList :book_id="parseInt(route.params.id[0])"/>
  </div>
</template>

<style scoped></style>
