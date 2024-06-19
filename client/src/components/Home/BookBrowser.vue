<script setup lang="ts">
import { ref } from 'vue'

const books = ref([1, 2, 3, 4])
</script>

<template>
  <div class="container">
    <h1>搜索结果</h1>
    <div class="result-container" v-for="book in books" :key="book">
      <div class="book-item">
        <el-col :span="4" class="book-img">image</el-col>
        <el-col :span="16">
          <RouterLink :to="{ name: 'detail', params: { id: book } }"><h2>书名</h2></RouterLink>
          <p>作者</p>
          <el-rate />
        </el-col>
        <el-col :span="4">
          <el-button class="reserve-btn" type="primary" size="mini">预约</el-button>
        </el-col>
      </div>
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
