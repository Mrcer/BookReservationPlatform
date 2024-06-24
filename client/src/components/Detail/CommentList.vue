<script setup lang="ts">
import { watch, ref, onUnmounted } from 'vue'
import { getComments } from '../../service/comment'
import type { CommentData } from '@/types'

const comments = ref<CommentData[]>([])
const props = defineProps<{
  book_id: number
}>()
const shouldFetchComments = ref(false)
// 创建一个定时器来每隔 30 秒拉取一次评论
const intervalId = setInterval(() => {
  shouldFetchComments.value = true // 每隔 30 秒设置 shouldFetchComments 为 true
}, 30000)
watch(shouldFetchComments, (flag, pre_flag) => {
  if (flag) {
    console.log('Fetching...')
    shouldFetchComments.value = false
    getComments(props.book_id).then((res) => {
      console.log(res)
      comments.value = res
    })
  }
})
// 在组件销毁时清除定时器
onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <div>
    <h2>Comments</h2>
    <ul>
      <li v-for="comment in comments">
        <el-row>
          <h3>
            <el-col>user-id:{{ comment.user_id }}</el-col>
            <el-col>time:{{ comment.date }}</el-col>
            <el-col>
              <el-rate v-model="comment.rating" show-score text-color="#ff9900" disabled />
            </el-col>
          </h3>
        </el-row>
        <p>{{ comment.content }}</p>
        <HR></HR>
      </li>
    </ul>
  </div>
</template>

<style scoped></style>
