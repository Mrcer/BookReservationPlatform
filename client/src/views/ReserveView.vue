<script setup lang="ts">
import ReservationCard from '@/components/Reserve/ReservationCard.vue'
import { getAllConfirmedReservations } from '@/service/reservation'
import { useUserStore } from '@/store';
import type { ReservationData } from '@/types';
import { onMounted, ref } from 'vue';

const isLoaded = ref(false)
const reservations = ref<ReservationData[]>([])

onMounted(async () => {
  const user = useUserStore()
  if(!user.isLoggedIn) {
    console.log('User not logged in')
    return
  }
  reservations.value = await getAllConfirmedReservations(user.uid)
    .catch((error) => {
      console.log(error.response.data.error)
      return []
    })
})

</script>

<template>
  <div class="main">
    <div v-if="!isLoaded">加载中...</div>
    <div class="container" v-else>
      <div v-if="reservations.length === 0">暂时没有预约记录</div>
      <ul>
        <ReservationCard
          book-name="The Great Gatsby"
          book-location="New York"
          reservation-location="San Francisco"
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
