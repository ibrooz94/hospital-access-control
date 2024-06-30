<script setup>
import { computed, reactive, ref } from 'vue'
import { mdiEye, mdiClose } from '@mdi/js'
import CardBoxModal from '@/components/CardBoxModal.vue'
import TableCheckboxCell from '@/components/TableCheckboxCell.vue'
import BaseLevel from '@/components/BaseLevel.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseButton from '@/components/BaseButton.vue'
import PillTag from '../PillTag.vue'
import BaseModal from '../BaseModal.vue'
import CardBox from '../CardBox.vue'
import FormField from '../FormField.vue'
import FormControl from '../FormControl.vue'
import CardBoxComponentTitle from '../CardBoxComponentTitle.vue'
import BaseDivider from '../BaseDivider.vue'

import { API } from '@/services'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
const toast = useToast()



const props = defineProps({
  checkable: Boolean,
  items: {
    type: Array
  }
})
const emit = defineEmits(['refreshApppointment'])

const isModalActive = ref(false)

const appointmentData = reactive({
  scheduled_date: null,
  status: null,
  id: null,
  assigned_doctor: null
})

const openAppointment = (client) => {
  appointmentData.scheduled_date = new Date(client.scheduled_date).toISOString().slice(0, 16)
  appointmentData.status = client.status
  appointmentData.id = client.id
  appointmentData.assigned_doctor = useAuthStore().authUser.id
  isModalActive.value = true
}

const submitAppointment = async (action) => {
  if (action) {
    try {
      if (action === "book") {
        appointmentData.status = "booked"
      }
      else if (action === "cancel") {
        appointmentData.status = "cancelled"
      }
      else if (action === "complete") {
        appointmentData.status = "completed"
      }
      const { id, ...dataToSend } = appointmentData;
      await API.appointment.patch(id, dataToSend);

      toast.success("Updated appointment!")
      emit('refreshApppointment')
      isModalActive.value = false

    }
    catch (err) {
      console.error("Update appointment failed: ", err.message)
      isModalActive.value = false
    }
  }
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
    case 'pending':
      return 'warning';
    case 'completed':
      return 'success';
    case 'cancelled':
      return 'danger';
    case 'booked':
      return 'info';
    default:
      return 'gray'; // Default color for unexpected status
  }
};
</script>

<template>

  <BaseModal v-model="isModalActive">
    <CardBox v-show="isModalActive" class="shadow-lg max-h-modal w-10/12 z-50" is-modal is-form>
      <CardBoxComponentTitle title="Update Appointment">
        <BaseButton :icon="mdiClose" color="whiteDark" small rounded-full @click.prevent="isModalActive = false" />
      </CardBoxComponentTitle>
      <BaseDivider />
      <FormField label="Scheduled Date">
        <FormControl v-model="appointmentData.scheduled_date" type="datetime-local" />
      </FormField>

      <template #footer>
        <BaseButtons v-has-role="['doctor']" v-if="appointmentData.status != 'cancelled'">
          <!-- book appointment -->
          <BaseButton type="button" label="Book" color="success" @click="submitAppointment('book')"
            v-if="appointmentData.status === 'pending'" />

          <!-- after appointment is completed -->
          <BaseButton type="button" label="Completed" color="success" @click="submitAppointment('complete')"
            v-if="appointmentData.status === 'booked'" />
          <BaseButton type="button" label="Cancel Appointment" color="danger" @click="submitAppointment('cancel')" />
        </BaseButtons>
      </template>
    </CardBox>

  </BaseModal>

  <CardBoxModal v-model="isModalDangerActive" title="Please confirm" button="danger" has-cancel>
    <p>Lorem ipsum dolor sit amet <b>adipiscing elit</b></p>
    <p>This is sample modal</p>
  </CardBoxModal>

  <table>
    <thead>
      <tr>
        <th v-if="checkable" />
        <th>On Behalf Of</th>
        <th>Reason</th>
        <th>Scheduled Time</th>
        <th>Status</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="client in itemsPaginated" :key="client.id">
        <TableCheckboxCell v-if="checkable" @checked="checked($event, client)" />
        <td data-label="On Behalf Of">
          {{ client.patient.email }}
        </td>
        <td data-label="Reason">
          {{ client.reason }}
        </td>
        <td class="lg:w-1 whitespace-nowrap" data-label="Date">
          <small class="text-gray-500 dark:text-slate-400" :title="client.created_at">{{
            new Date(client.scheduled_date).toLocaleString()
            }}</small>
        </td>
        <td data-label="Status" class="lg:w-1">
          <PillTag :color="getStatusColor(client.status)" :label="client.status" />
        </td>
        <td class="lg:w-1 whitespace-nowrap">
          <BaseButtons type="justify-start lg:justify-end" no-wrap>
            <BaseButton color="info" :icon="mdiEye" small @click="openAppointment(client)" />
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
