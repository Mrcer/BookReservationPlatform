<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <AppHeader />
  <RouterView />
  <AppFooter />
</template>
