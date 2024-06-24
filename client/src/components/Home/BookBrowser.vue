<script setup lang="ts">
import Book from './Book.vue'
import type { BookData } from '@/types';

const props = defineProps<{
  books: BookData[]
}>()

</script>

<template>
  <div class="container">
    <h1>搜索结果</h1>
    <div class="result-container" v-for="book in props.books" :key="book.id">
      <Book :book="book" />
    </div>
    <div v-if="props.books.length === 0">
      <p>没有搜索结果</p>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  max-width: 800px;
}

.result-container {
  width: 100%;
}
</style>
