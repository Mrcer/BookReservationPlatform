<script setup lang="ts">
import { submitReservation } from '@/service/reservation'
import { useUserStore } from '@/store'
import type { BookData } from '@/types'
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const user = useUserStore()
const props = defineProps<{
  book: BookData | null
}>()

const isVisible = defineModel()
const showForm = ref(false)
const location = ref('')
const handleConfirm = async () => {
  let message
  if (user.isLoggedIn) {
    message = await submitReservation(user.uid, props.book!.id, location.value)
      .then((res) => {
        return '预约成功'
      })
      .catch((error) => {
        console.error(error.response.data)
        return '您已预约过该图书，请勿重复预约'
      })
  } else {
    message = '请先登录后再进行预约'
  }
  await ElMessageBox.alert(message, {
    confirmButtonText: '确认',
  }).catch(() => {
    // cancel, do nothing
    return
  })
  isVisible.value = false
}
</script>

<template>
  <div class="backdrop" v-if="isVisible">
    <div class="container">
      <div style="margin-bottom: 0.5rem">
        <p style="text-align: center">您确认要预约位于</p>
        <p style="text-align: center; font-weight: bold">{{ book?.location }}</p>
        <p style="text-align: center">
          的
          <span style="font-weight: bold">《{{ book?.title }}》</span>
          吗？
        </p>
      </div>
      <div>
        <span>请输入预约地点：</span>
        <el-input
          style="display: inline; margin-right: 10px"
          v-model="location"
          placeholder="预约地点"
        ></el-input>
      </div>
      <div>
        <el-button style="display: inline; margin: 10px" @click="isVisible = false">取消</el-button>
        <el-button style="display: inline; margin: 10px" type="primary" @click="handleConfirm">
          确认
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: medium;
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 400px;
}
</style>
