<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth';
import BaseLevel from '@/components/BaseLevel.vue'
import UserAvatarCurrentUser from '@/components/UserAvatarCurrentUser.vue'
import CardBox from '@/components/CardBox.vue'

const authStore = useAuthStore()

const userName = computed(() => authStore.authUser.email)

</script>

<template>
  <CardBox>
    <BaseLevel type="justify-around lg:justify-center">
      <UserAvatarCurrentUser class="lg:mx-12" />
      <div class="space-y-3 text-center md:text-left lg:mx-12">

        <h1 class="text-2xl">
          Howdy, <b>{{ userName }}</b>!
        </h1>
        <!-- <p>Last login <b>12 mins ago</b> from <b>127.0.0.1</b></p> -->
      </div>
    </BaseLevel>
  </CardBox>
</template>
