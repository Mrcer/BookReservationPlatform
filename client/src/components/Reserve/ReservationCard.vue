<script setup lang="ts">
const props = defineProps<{
  bookName: string
  bookLocation: string
  reservationLocation: string
}>()
</script>

<template>
  <el-card>
    <p>
      希望好心人把位于
      <span class="highlight book-location">{{ props.bookLocation }}</span>
      的
      <span class="highlight book-name">《{{ props.bookName }}》</span>
      送到
      <span class="highlight reservation-location">{{ props.reservationLocation }}</span>
    </p>
    <p style="text-align: right">发布时间：2022-01-01</p>
  </el-card>
</template>

<style scoped>
.highlight {
  font-weight: bold;
  padding: 0.5rem;
  margin-bottom: 1rem;
}

.book-location {
  color: #409eff;
}

.book-name {
  color: #67c23a;
}

.reservation-location {
  color: #f56c6c;
}
</style>
