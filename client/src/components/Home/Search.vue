<script setup lang="ts">
import { ref } from 'vue'
import { type SearchQuery } from '../type'

const search_input = ref('')

const emit = defineEmits(['search'])
const handleSearch = () => {
  const query: SearchQuery = {
    keyword: search_input.value,
  }
  emit('search', query)
}
</script>

<template>
  <div class="container">
    <div class="search-container">
      <el-input v-model="search_input" class="search-input" placeholder="搜索书籍" clearable />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 80%;
  max-width: 800px;
}

.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
</style>
