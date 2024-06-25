<script setup lang="ts">
import { BookStatus, type BookData } from '@/types'
import { computed, onMounted, ref } from 'vue'
import { getInfo } from '@/service/book'

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
  <el-row class="book-detail">
    <el-col :span="16">
      <h1>{{ props.book.title }}</h1>
      <p data-test="author">作者：{{ props.book.author }}</p>
      <p data-test="publisher">出版社：{{ props.book.publisher }}</p>
      <p data-test="publishDate">出版日期：{{ props.book.publishDate }}</p>
      <p data-test="isbn">ISBN：{{ props.book.isbn }}</p>
      <el-rate
        v-model="props.book.rating"
        show-score
        text-color="#ff9900"
        disabled
        v-if="props.book.rating != -1"
      />
      <div v-else>
        <el-rate :model-value="0" disabled />
        <span style="color: #999">暂无评分</span>
      </div>
      <el-button
        data-test="reserve-btn"
        class="reserve-btn"
        type="primary"
        size="large"
        style="display: block"
        :disabled="!canBeReserved"
        @click="$emit('reserve')"
      >
        {{ buttonText }}
      </el-button>
    </el-col>
    <el-col :span="8" class="book-img">
      <el-image :src="'data:image/jpeg;base64,' + book.cover" />
    </el-col>
  </el-row>
</template>

<style scoped></style>
