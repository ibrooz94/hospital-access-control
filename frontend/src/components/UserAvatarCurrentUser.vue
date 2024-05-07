<script setup>
import { useAuthStore } from '@/stores/auth';
import UserAvatar from '@/components/UserAvatar.vue'

const authStore = useAuthStore()
</script>

<template>
  <!-- <UserAvatar :username="mainStore.userName" :avatar="mainStore.userAvatar"> -->
  <UserAvatar :username="authStore.authUser?.email">
    <slot />
  </UserAvatar>
</template>
