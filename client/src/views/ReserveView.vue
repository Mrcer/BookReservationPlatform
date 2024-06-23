<script setup lang="ts">
import ReservationCard from '@/components/Reserve/ReservationCard.vue'
</script>

<template>
  <div class="main">
    <div class="container">
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
