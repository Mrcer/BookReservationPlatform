<script setup lang="ts">
import { getBorrowed } from '@/service/book'
import { useUserStore } from '@/store'
import type { BookData, ReservationData } from '@/types'
import { onMounted, ref } from 'vue'

const bookNames = ref<string[]>([])

onMounted(async () => {
  let user = useUserStore()
  const res = await getBorrowed(user.uid).catch((error) => {
    console.log(error.response.data.error)
    return []
  })
  res.forEach((item) => bookNames.value.push(item.title))
})
</script>

<template>
  <div class="warpper">
    <h2 v-if="bookNames.length === 0">~空空如也~</h2>
    <ul>
      <li v-for="(name, index) in bookNames" :key="index">{{ name }}</li>
    </ul>
  </div>
</template>

<style scoped>
.warpper {
  padding: 20px;
}
</style>
