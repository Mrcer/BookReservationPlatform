<script setup lang="ts">
import { ref } from 'vue'

const comments = ref(['aaa', 'bbb', 'ccc'])
const props = defineProps<{
  book_id : number
}>()
</script>

<template>
  <div>
    <h2>Comments</h2>
    <ul>
      <li v-for="comment in comments">
        {{ comment }}
      </li>
    </ul>
  </div>
</template>

<style scoped></style>
