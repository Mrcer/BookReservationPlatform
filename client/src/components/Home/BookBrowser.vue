<script setup lang="ts">
import { ref } from 'vue'

const books = ref([1, 2, 3, 4])
</script>

<template>
  <div>
    <h1>搜索结果</h1>
    <tr v-for="book in books" :key="book">
      <td>
        <span>{{ book }}</span>
        <RouterLink :to="{ name: 'detail', params: { id: book } }">详情</RouterLink>
        <input type="button" value="预约" @click="console.log('预约功能暂未开通，敬请期待！')" />
      </td>
    </tr>
  </div>
</template>

<style scoped></style>
