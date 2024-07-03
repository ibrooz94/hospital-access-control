<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { mdiAccount, mdiAsterisk } from '@mdi/js'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
// import FormCheckRadio from '@/components/FormCheckRadio.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'

import { useAuthStore } from '@/stores/auth'

const form = reactive({
  login: '',
  pass: '',
  remember: true
})

const router = useRouter()
const authStore = useAuthStore()

const submit = async () => {

  const data = new FormData()
  data.append('username', form.login);
  data.append('password', form.pass);

  const request = await authStore.dispatchLogin(data)
  if (request.success) {
    const userRequest = await authStore.dispatchCurrentUser()
    if (userRequest.success) {
      if (userRequest.content.role.id != 4 || userRequest.content.role.id != 1) {
        router.push('/visits')
      }
      else {
        router.push('/appointments')
      }
    }
  }
}
</script>

<template>
  <LayoutGuest>
    <SectionFullScreen v-slot="{ cardClass }" bg="pinkRed">
      <CardBox :class="cardClass" is-form @submit.prevent="submit">
        <FormField label="Login" help="Please enter your login">
          <FormControl v-model="form.login" :icon="mdiAccount" name="login" autocomplete="username" required />
        </FormField>

        <FormField label="Password" help="Please enter your password">
          <FormControl v-model="form.pass" :icon="mdiAsterisk" type="password" name="password" required
            autocomplete="current-password" />
        </FormField>

        <!-- <FormCheckRadio v-model="form.remember" name="remember" label="Remember" :input-value="false" /> -->

        <template #footer>
          <BaseButtons>
            <BaseButton type="submit" color="info" label="Login" />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>
