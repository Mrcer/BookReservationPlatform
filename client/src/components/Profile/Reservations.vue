<script setup lang="ts">
import type { BookData, ReservationData } from '@/types'
import { ref } from 'vue'

interface TableData {
  reserved_date: string
  bookName: string
  bookLocation: string
  reservationLocation: string
}

// TODO: get data from server
const reservations = ref<TableData[]>([
  {
    reserved_date: '2022-01-01',
    bookName: '《三体》',
    bookLocation: '图书馆',
    reservationLocation: '101教室',
  },
])
</script>

<template>
  <div class="warpper">
    <h2 v-if="reservations.length === 0">~空空如也~</h2>
    <el-table :data="reservations" style="width: 100%">
      <el-table-column prop="reserved_date" label="预约日期" width="150" />
      <el-table-column prop="bookName" label="书名" width="150" />
      <el-table-column prop="bookLocation" label="书籍位置" width="150" />
      <el-table-column prop="reservationLocation" label="预约位置" width="150" />
    </el-table>
  </div>
</template>

<style scoped>
.warpper {
  padding: 20px;
}
</style>
