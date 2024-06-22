<script setup lang="ts">
import { type BookData } from '@/types'
import { ref } from 'vue'

const props = defineProps<{
  book: BookData
}>()
</script>

<template>
  <el-row class="book-container">
    <!-- TODO: add image -->
    <el-col :span="4" class="book-img">image</el-col>
    <el-col :span="16">
      <RouterLink :to="{ name: 'detail', params: { id: props.book.id } }">
        <h2>{{ props.book.title }}</h2>
      </RouterLink>
      <p>作者：{{ props.book.author }}</p>
      <p>出版社：{{ props.book.publisher }}</p>
      <p>出版日期：{{ props.book.publishDate }}</p>
      <p>ISBN：{{ props.book.isbn }}</p>
      <!-- TODO: add rating -->
      <el-rate />
    </el-col>
    <el-col :span="4">
      <el-button class="reserve-btn" type="primary" size="large">预约</el-button>
    </el-col>
  </el-row>
</template>

<style scoped>
.book-item {
  display: flex;
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.book-img {
  width: 100px;
  height: 150px;
}
</style>
