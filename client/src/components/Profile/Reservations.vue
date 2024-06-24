<script setup lang="ts">
import type { BookData, ReservationData } from '@/types'
import { useUserStore } from '@/store'
import { onMounted, ref } from 'vue'
import { getUserReservations } from '@/service/reservation'
import { getInfo } from '@/service/book'

interface TableData {
  reserved_date: string
  bookName: string
  bookLocation: string
  reservationLocation: string
}

const reservations = ref<TableData[]>([])

onMounted(async () => {
  const user = useUserStore()
  if (!user.isLoggedIn) {
    console.log('User not logged in')
    return
  }
  let reservationsData: ReservationData[] = await getUserReservations(user.uid).catch((error) => {
    console.log(error.response.data.error)
    return []
  })
  Promise.all(
    reservationsData.map(async (reservation) => {
      let bookInfo = await getInfo(reservation.bookId)
      let data = {
        bookName: bookInfo.title,
        bookLocation: reservation.book_location,
        reservationLocation: reservation.reservation_location,
        reserved_date: reservation.reserved_date,
      }
      reservations.value.push(data)
    })
  )
  reservations.value.sort(
    (a, b) => new Date(a.reserved_date).getTime() - new Date(b.reserved_date).getTime()
  )
})
</script>

<template>
  <div class="warpper">
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
