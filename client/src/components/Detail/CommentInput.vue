<script setup lang="ts">
import { ref } from 'vue'
import { sendComment } from '@/service/comment'
import { useUserStore } from '../../store/index'

const textarea = ref('')
const rate = ref(0)
const props = defineProps<{
  book_id: number
}>()
const userStore = useUserStore()
</script>

<template>
  <div class="rate">
    评价：
    <el-rate v-model="rate" show-score text-color="#ff9900" />
  </div>
  <div>
    <el-input
      v-model="textarea"
      maxlength="50"
      style="width: 480px"
      :rows="3"
      type="textarea"
      show-word-limit
      placeholder="Please input"
    />
    <el-button
      data-test="reserve-btn"
      class="reserve-btn"
      type="primary"
      size="large"
      @click="
        sendComment({ userId: userStore.uid, bookId: book_id, content: textarea, rating: rate })
      "
    >
      {{ '发送' }}
    </el-button>
  </div>
</template>

<style scoped></style>
