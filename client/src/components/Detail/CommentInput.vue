<script setup lang="ts">
import { computed, ref } from 'vue'
import { sendComment } from '@/service/comment'
import { useUserStore } from '../../store/index'
import { ElMessageBox } from 'element-plus'

const textarea = ref('')
const rate = ref(0)
const props = defineProps<{
  book_id: number
  disable: boolean
}>()
const userStore = useUserStore()
const placeholder = computed(() => {
  if (props.disable) {
    return '请先登录'
  } else {
    return '请输入评论内容'
  }
})
const handleSendComment = async () => {
  let message = await sendComment({
    userId: userStore.uid,
    bookId: props.book_id,
    content: textarea.value,
    rating: rate.value,
  })
    .then(() => {
      return '评论成功'
    })
    .catch((err) => {
      return '评论失败：' + err.response.data.message
    })
  await ElMessageBox.alert(message, {
    confirmButtonText: '确认',
  }).catch(() => {
    // cancel, do nothing
    return
  })
}
</script>

<template>
  <div class="container">
    <div class="rate">
      评价：
      <el-rate v-model="rate" show-score text-color="#ff9900" :disabled="disable" />
    </div>
    <div>
      <el-input
        v-model="textarea"
        maxlength="50"
        style="width: 480px"
        :rows="3"
        type="textarea"
        show-word-limit
        :placeholder="placeholder"
        :disabled="disable"
      />
      <el-button
        data-test="reserve-btn"
        class="reserve-btn"
        type="primary"
        size="large"
        :disabled="disable"
        @click="handleSendComment"
      >
        {{ '发送' }}
      </el-button>
    </div>
  </div>
</template>

<style scoped></style>
