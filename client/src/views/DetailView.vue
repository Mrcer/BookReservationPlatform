<script setup lang="ts">
import { useRoute } from 'vue-router'
import CommentInput from '@/components/Detail/CommentInput.vue'
import CommentList from '@/components/Detail/CommentList.vue'
import Detail from '@/components/Detail/Detail.vue'
import type { BookData } from '@/types'
import { onMounted, ref } from 'vue'
import { getInfo } from '@/service/book'
import ReservationComfirm from '@/components/ReservationComfirm.vue'
import { useUserStore } from '@/store'

const route = useRoute()

const book = ref<BookData | null>(null)
const showComfirm = ref(false)
const user = useUserStore()

onMounted(() => {
  getInfo(parseInt(route.params.id[0]))
    .then((res) => (book.value = res))
    .catch((err) => console.error(err))
})
</script>

<template>
  <div class="main">
    <div>
      <Detail v-if="book" :book="book!" style="margin-bottom: 4rem" @reserve="showComfirm = true" />
      <CommentInput
        :book_id="parseInt(route.params.id[0])"
        style="margin-bottom: 2rem"
        :disable="!user.isLoggedIn"
      />
      <CommentList :book_id="parseInt(route.params.id[0])" />
      <ReservationComfirm v-model="showComfirm" :book="book" />
    </div>
  </div>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 6rem;
}
</style>
