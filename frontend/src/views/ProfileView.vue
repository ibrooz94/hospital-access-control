<script setup>
import { reactive } from 'vue'
import { mdiAccount, mdiMail, mdiAsterisk, mdiFormTextboxPassword } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import BaseDivider from '@/components/BaseDivider.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import UserCard from '@/components/UserCard.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLine from '@/components/SectionTitleLine.vue'
import { useAuthStore } from '@/stores/auth'


const authStore = useAuthStore()

const profileForm = reactive({
    name: `${authStore.authUser.first_name} ${authStore.authUser.last_name}`,
    email: authStore.authUser.email
})

const passwordForm = reactive({
    password_current: '',
    password: '',
    password_confirmation: ''
})

const submitProfile = () => {
    // update user profile
    // authStore.setUser(profileForm)
}

const submitPass = () => {
    // update password
}
</script>

<template>
    <LayoutAuthenticated>
        <SectionMain>
            <SectionTitleLine :icon="mdiAccount" title="Profile" main>
            </SectionTitleLine>

            <UserCard class="mb-6" />

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <CardBox is-form @submit.prevent="submitProfile">
                    <FormField label="Name" help="Required. Your name">
                        <FormControl v-model="profileForm.name" :icon="mdiAccount" name="username" required
                            autocomplete="username" />
                    </FormField>
                    <FormField label="E-mail" help="Required. Your e-mail">
                        <FormControl v-model="profileForm.email" :icon="mdiMail" type="email" name="email" required
                            autocomplete="email" disabled />
                    </FormField>

                    <template #footer>
                        <BaseButtons>
                            <BaseButton color="info" type="submit" label="Submit" />
                            <BaseButton color="info" label="Options" outline />
                        </BaseButtons>
                    </template>
                </CardBox>

                <CardBox is-form @submit.prevent="submitPass">
                    <FormField label="Current password" help="Required. Your current password">
                        <FormControl v-model="passwordForm.password_current" :icon="mdiAsterisk" name="password_current"
                            type="password" required autocomplete="current-password" />
                    </FormField>

                    <BaseDivider />

                    <FormField label="New password" help="Required. New password">
                        <FormControl v-model="passwordForm.password" :icon="mdiFormTextboxPassword" name="password"
                            type="password" required autocomplete="new-password" />
                    </FormField>

                    <FormField label="Confirm password" help="Required. New password one more time">
                        <FormControl v-model="passwordForm.password_confirmation" :icon="mdiFormTextboxPassword"
                            name="password_confirmation" type="password" required autocomplete="new-password" />
                    </FormField>

                    <template #footer>
                        <BaseButtons>
                            <BaseButton type="submit" color="info" label="Submit" />
                            <BaseButton color="info" label="Options" outline />
                        </BaseButtons>
                    </template>
                </CardBox>
            </div>
        </SectionMain>
    </LayoutAuthenticated>
</template>
