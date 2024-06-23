<script setup lang="ts">
import type { BookData, ReservationData } from '@/types'
import { ref } from 'vue'

// TODO: get data from server
const bookName = ref<string[]>(['《三体》', '《三体II：死神永生》', '《三体III：死神来了》'])
</script>

<template>
  <div class="warpper">
    <h2 v-if="bookName.length === 0">~空空如也~</h2>
    <ul>
      <li v-for="(name, index) in bookName" :key="index">{{ name }}</li>
    </ul>
  </div>
</template>

<style scoped>
.warpper {
  padding: 20px;
}
</style>
