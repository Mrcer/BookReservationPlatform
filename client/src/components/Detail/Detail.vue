<script setup lang="ts">
import { BookStatus, type BookData } from '@/types'
import { computed, ref } from 'vue'
import { getInfo } from '@/service/book'

const props = defineProps<{
  book_id : number
}>()
const book = ref<BookData>({} as BookData)
getInfo(props.book_id)
.then((res)=>{
    book.value = res
    console.log(res)
})
const canBeReserved = computed(() => {
  return book.value.status == BookStatus.Available || book.value.status == BookStatus.Reserved
})

const buttonText = computed(() => {
  if (canBeReserved.value) {
    return '预约'
  } else if (book.value.status == BookStatus.Borrowed) {
    return '已借出'
  } else if (book.value.status == BookStatus.Damaged) {
    return '无法借阅'
  }
})
</script>

<template>
    <el-row class="book-detail">
        <el-col :span="8" class="book-img">
            <el-image :src="book.cover" />
        </el-col>
        <el-col :span="16">
            <h2>{{ book.title }}</h2>
            <p data-test="author">作者：{{ book.author }}</p>
            <p data-test="publisher">出版社：{{ book.publisher }}</p>
            <p data-test="publishDate">出版日期：{{ book.publishDate }}</p>
            <p data-test="isbn">ISBN：{{ book.isbn }}</p>
            <el-rate v-model="book.rating" show-score text-color="#ff9900" disabled />
        </el-col>
        <el-button
        data-test="reserve-btn"
        class="reserve-btn"
        type="primary"
        size="large"
        :disabled="!canBeReserved"
        @click="$emit('reserve', book.id)"
        >
            {{ buttonText }}
        </el-button>
    </el-row>
</template>

<style scoped></style>
