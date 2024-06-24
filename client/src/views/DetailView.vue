<script setup lang="ts">
import { useRoute } from 'vue-router'
import CommentInput from '@/components/Detail/CommentInput.vue'
import CommentList from '@/components/Detail/CommentList.vue'
import Detail from '@/components/Detail/Detail.vue'
const route = useRoute()
</script>

<template>
  <div class="main">
    <div>
      <Detail :book_id="parseInt(route.params.id[0])" style="margin-bottom: 4rem;" />
      <CommentInput :book_id="parseInt(route.params.id[0])" style="margin-bottom: 2rem;" />
      <CommentList :book_id="parseInt(route.params.id[0])" />
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
