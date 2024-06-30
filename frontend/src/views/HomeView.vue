<script setup>
import { computed, ref, onMounted } from 'vue'
import {
  mdiAccountMultiple,
  mdiChartTimelineVariant,
} from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxTransaction from '@/components/CardBoxTransaction.vue'
import CardBoxClient from '@/components/CardBoxClient.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBoxComponentEmpty from '@/components/CardBoxComponentEmpty.vue'
import TablePatients from '@/components/tables/TablePatients.vue'
import { API } from '@/services'

// import router from '@/router'

const vitals = ref(null)


onMounted(async () => {
  vitals.value = await API.vital.listByVisit(1)
  console.log(vitals.value)
})


const clientBarItems = computed(() => [])
const transactionBarItems = computed(() => [])

</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLineWithButton :icon="mdiChartTimelineVariant" title="Appointments" main>
      </SectionTitleLineWithButton>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
        <CardBoxWidget color="text-blue-500" :icon="mdiAccountMultiple" :number="1" label="Booked" />
        <CardBoxWidget color="text-yellow-500" :icon="mdiAccountMultiple" :number="1" label="Pending" />
        <CardBoxWidget color="text-emerald-500" :icon="mdiAccountMultiple" :number="12" label="Completed" />
        <CardBoxWidget color="text-red-500" :icon="mdiAccountMultiple" :number="1" label="Cancelled" />
        <!-- <CardBoxWidget color="text-red-500" :icon="mdiChartTimelineVariant" :number="256" suffix="%"
          label="Performance" /> -->
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div class="flex flex-col justify-between">
          <CardBoxTransaction v-for="(transaction, index) in transactionBarItems" :key="index"
            :amount="transaction.amount" :date="transaction.date" :business="transaction.business"
            :type="transaction.type" :name="transaction.name" :account="transaction.account" />
        </div>
        <div class="flex flex-col justify-between">
          <CardBoxClient v-for="client in clientBarItems" :key="client.id" :name="client.name" :login="client.login"
            :date="client.created" :progress="client.progress" />
        </div>
      </div>


      <SectionTitleLineWithButton :icon="mdiAccountMultiple" title="Patients" />

      <CardBox has-table>
        <TablePatients v-if="vitals" :items="vitals.data" />
        <CardBoxComponentEmpty v-else />
      </CardBox>

    </SectionMain>
  </LayoutAuthenticated>
</template>
