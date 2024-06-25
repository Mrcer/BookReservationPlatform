<script setup lang="ts">
import ReservationCard from '@/components/Reserve/ReservationCard.vue'
import { getAllConfirmedReservations } from '@/service/reservation'
import { getInfo } from '@/service/book'
import { useUserStore } from '@/store'
import type { ReservationData } from '@/types'
import { onMounted, ref } from 'vue'

const isLoaded = ref(false)
const reservationCardData = ref<
  {
    reservationId: number
    bookName: string
    bookLocation: string
    reservationLocation: string
    reservationTime: string
  }[]
>([])

onMounted(async () => {
  const user = useUserStore()
  if (!user.isLoggedIn) {
    console.log('User not logged in')
    return
  }
  let reservationsData: ReservationData[] = await getAllConfirmedReservations(user.uid).catch(
    (error) => {
      console.log(error.response.data.error)
      isLoaded.value = true
      return []
    }
  )
  Promise.all(
    reservationsData.map(async (reservation) => {
      let bookInfo = await getInfo(reservation.bookId)
      let data = {
        reservationId: reservation.reservationId,
        bookName: bookInfo.title,
        bookLocation: reservation.book_location,
        reservationLocation: reservation.reservation_location,
        reservationTime: reservation.reservation_date,
      }
      reservationCardData.value.push(data)
    })
  )
  reservationsData.sort(
    (a, b) => new Date(a.reservation_date).getTime() - new Date(b.reservation_date).getTime()
  )
  isLoaded.value = true
})
</script>

<template>
  <div class="main">
    <div v-if="!isLoaded">加载中...</div>
    <div class="container" v-else>
      <div v-if="reservationCardData.length === 0">暂时没有预约记录</div>
      <ul>
        <ReservationCard
          v-for="reservation in reservationCardData"
          :key="reservation.reservationId"
          :bookName="reservation.bookName"
          :bookLocation="reservation.bookLocation"
          :reservationLocation="reservation.reservationLocation"
          :reservationTime="reservation.reservationTime"
        />
      </ul>
    </div>
  </div>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 4rem;
}

.container {
  width: 80%;
  max-width: 800px;
}
</style>
