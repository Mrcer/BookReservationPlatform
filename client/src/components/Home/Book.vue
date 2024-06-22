<script setup lang="ts">
import { BookStatus, type BookData } from '@/types'
import { ca, de } from 'element-plus/es/locales.mjs';
import { computed, ref } from 'vue'

const props = defineProps<{
  book: BookData
}>()

defineEmits(['reserve'])

const canBeReserved = computed(() => {
  return props.book.status == BookStatus.Available || props.book.status == BookStatus.Reserved
})

const buttonText = computed(() => {
  if (canBeReserved.value) {
    return '预约'
  } else if (props.book.status == BookStatus.Borrowed) {
    return '已借出'
  } else if (props.book.status == BookStatus.Damaged) {
    return '无法借阅'
  }
})

</script>

<template>
  <el-row class="book-container">
    <el-col :span="4" class="book-img">
      <el-image :src="book.cover" />
    </el-col>
    <el-col :span="16">
      <RouterLink :to="{ name: 'detail', params: { id: props.book.id } }">
        <h2>{{ props.book.title }}</h2>
      </RouterLink>
      <p>作者：{{ props.book.author }}</p>
      <p>出版社：{{ props.book.publisher }}</p>
      <p>出版日期：{{ props.book.publishDate }}</p>
      <p>ISBN：{{ props.book.isbn }}</p>
      <el-rate v-model="props.book.rating" show-score text-color="#ff9900" disabled/>
    </el-col>
    <el-col :span="4">
      <el-button
        class="reserve-btn"
        type="primary"
        size="large"
        :disabled="!canBeReserved"
        @click="$emit('reserve', props.book.id)">{{ buttonText }}</el-button>
    </el-col>
  </el-row>
</template>

<style scoped>
.book-item {
  display: flex;
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.book-img {
  padding: 0.5rem;
}

.reserve-btn {
  width: 8rem;
}
</style>
