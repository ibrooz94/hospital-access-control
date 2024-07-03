<script setup>
import { computed, ref } from 'vue'
import { mdiEye } from '@mdi/js'
import CardBoxModal from '@/components/CardBoxModal.vue'
import TableCheckboxCell from '@/components/TableCheckboxCell.vue'
import BaseLevel from '@/components/BaseLevel.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseButton from '@/components/BaseButton.vue'
import PillTag from '../PillTag.vue'

import router from '@/router'


const props = defineProps({
  checkable: Boolean,
  items: {
    type: Array
  }
})

const openVisit = (visitId) => {
  router.push(`/visits/${visitId}`);
}

const items = computed(() => props.items)

const isModalDangerActive = ref(false)

const perPage = ref(8)

const currentPage = ref(0)

const checkedRows = ref([])

const itemsPaginated = computed(() =>
  items.value.slice(perPage.value * currentPage.value, perPage.value * (currentPage.value + 1))
)

const numPages = computed(() => Math.ceil(items.value.length / perPage.value))

const currentPageHuman = computed(() => currentPage.value + 1)


const pagesList = computed(() => {
  const pagesList = []

  for (let i = 0; i < numPages.value; i++) {
    pagesList.push(i)
  }

  return pagesList
})

const remove = (arr, cb) => {
  const newArr = []

  arr.forEach((item) => {
    if (!cb(item)) {
      newArr.push(item)
    }
  })

  return newArr
}

const checked = (isChecked, client) => {
  if (isChecked) {
    checkedRows.value.push(client)
  } else {
    checkedRows.value = remove(checkedRows.value, (row) => row.id === client.id)
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case 'admitted':
      return 'warning';
    case 'discharged':
      return 'success';
    case 'checked_in':
      return 'warning';
    case 'checked_out':
      return 'success';
    default:
      return 'gray'; // Default color for unexpected status
  }
};
</script>

<template>

  <CardBoxModal v-model="isModalDangerActive" title="Please confirm" button="danger" has-cancel>
    <p>Lorem ipsum dolor sit amet <b>adipiscing elit</b></p>
    <p>This is sample modal</p>
  </CardBoxModal>

  <table>
    <thead>
      <tr>
        <th v-if="checkable" />
        <th>Id</th>
        <th>Patient</th>
        <th>Status</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="client in itemsPaginated" :key="client.id">
        <TableCheckboxCell v-if="checkable" @checked="checked($event, client)" />
        <td data-label="Id">
          {{ client.id }}
        </td>
        <td data-label="Patient">
          {{ client.patient.email }}
        </td>
        <td data-label="Status" class="lg:w-1">
          <PillTag :color="getStatusColor(client.visit_status)" :label="client.visit_status" />
        </td>
        <td class="lg:w-1 whitespace-nowrap">
          <BaseButtons type="justify-start lg:justify-end" no-wrap>
            <BaseButton color="info" :icon="mdiEye" small @click="openVisit(client.id)" />
            <!-- <BaseButton color="danger" :icon="mdiTrashCan" small @click="isModalDangerActive = true" /> -->
          </BaseButtons>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="p-3 lg:px-6 border-t border-gray-100 dark:border-slate-800">
    <BaseLevel>
      <BaseButtons>
        <BaseButton v-for="page in pagesList" :key="page" :active="page === currentPage" :label="page + 1"
          :color="page === currentPage ? 'lightDark' : 'whiteDark'" small @click="currentPage = page" />
      </BaseButtons>
      <small>Page {{ currentPageHuman }} of {{ numPages }}</small>
    </BaseLevel>
  </div>
</template>
