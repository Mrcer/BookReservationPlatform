<script setup lang="ts">
import Search from '@/components/Home/Search.vue'
import BookBrowser from '@/components/Home/BookBrowser.vue'
import { ref } from 'vue'
import type { SearchQuery, BookData } from '@/types'
import { search } from '@/service/book'
import ReservationComfirm from '@/components/ReservationComfirm.vue'

const searchResult = ref<BookData[]>([])
const searched = ref(false)
const showComfirm = ref(false)
const comfirmBook = ref<BookData | null>(null)

const handleSearch = (query: SearchQuery) => {
  search(query.keyword)
    .then((result) => {
      searched.value = true
      searchResult.value = result
    })
    .catch((error) => {
      if (error.response.status === 404) {
        searched.value = true
        searchResult.value = []
      } else {
        alert('搜索失败')
        console.error(error)
      }
    })
}

const handleReserve = (book: BookData) => {
  showComfirm.value = true
  comfirmBook.value = book
}
</script>

<template>
  <div class="main">
    <div>
      <h1 class="title">图书预约系统</h1>
    </div>
    <Search @search="handleSearch" />
    <!-- <h2>推荐活动啥的，在搜索后隐藏</h2> -->
    <!-- 设计要求在这里嵌入的预约组件可能需要附着在某个按钮上，点击按钮后弹出预约组件 -->
    <BookBrowser :books="searchResult" v-if="searched" @reserve="handleReserve" />
    <ReservationComfirm v-model="showComfirm" :book="comfirmBook" />
  </div>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  font-size: 6rem;
  font-weight: lighter;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  margin-top: 4rem;
  margin-bottom: 4rem;
}
</style>
