<script setup lang="ts">
import { ref } from 'vue'
import Book from './Book.vue';
import { getMockBookData } from '@/tests/mock/Book';

const books = ref([1, 2, 3, 4])
</script>

<template>
  <div class="container">
    <h1>搜索结果</h1>
    <div class="result-container" v-for="book in getMockBookData() " :key="book.id">
      <Book :book="book" />
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
