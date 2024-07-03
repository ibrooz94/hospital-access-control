<script setup>
import { computed, ref, reactive, onMounted } from 'vue'
import {
  mdiAccountMultiple,
  mdiChartTimelineVariant,
  mdiClose
} from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBox from '@/components/CardBox.vue'
import BaseModal from '@/components/BaseModal.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLine from '@/components/SectionTitleLine.vue'
import CardBoxComponentEmpty from '@/components/CardBoxComponentEmpty.vue'
import CardBoxComponentTitle from '@/components/CardBoxComponentTitle.vue'
import TableAppointments from '@/components/tables/TableAppointments.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseDivider from '@/components/BaseDivider.vue'
import { API } from '@/services'
import { useToast } from 'vue-toastification'

const toast = useToast()


const appointments = ref(null)
const queryParams = reactive({
  params: {
    status: null,
    date_from: null,
    date_to: null,
    sort: "-updated_at"
  }
});
const createAppointmentForm = reactive({
  reason: "",
  scheduled_date: null,
  on_behalf_of: null
})

const statusOptions = [
  { value: null, label: "Status" },
  { value: "pending", label: "Pending" },
  { value: "cancelled", label: "Cancelled" },
  { value: "booked", label: "Booked" },
]

const fetchAppointments = async () => {
  try {
    appointments.value = await API.appointment.list(queryParams)
  } catch (err) {
    console.error("Error fetching apppintments: ", err.message)
  }
}

const submitAppointmentForm = async () => {
  try {
    await API.appointment.create(createAppointmentForm)
    createAppointmentModal.value = false
    fetchAppointments()
    toast.success("Appointment created")

  } catch (err) {
    createAppointmentModal.value = false
    console.error("Error creating appointment", err.message)
  }
}


onMounted(async () => {
  await fetchAppointments();
})

const hasAppointments = computed(() => appointments.value?.data.length > 0);
const pendingCount = computed(() => appointments.value?.data.filter(appointment => appointment.status === 'pending').length || 0);
const bookedCount = computed(() => appointments.value?.data.filter(appointment => appointment.status === 'booked').length || 0);

const createAppointmentModal = ref(false)

</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLine :icon="mdiChartTimelineVariant" title="Appointments" main>
      </SectionTitleLine>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
        <CardBoxWidget color="text-blue-500" :icon="mdiAccountMultiple" :number="bookedCount" label="Booked" />
        <CardBoxWidget color="text-yellow-500" :icon="mdiAccountMultiple" :number="pendingCount" label="Pending" />
      </div>

      <BaseModal v-model="createAppointmentModal">
        <CardBox v-show="createAppointmentModal" class="shadow-lg max-h-modal w-10/12 z-50" is-modal is-form
          @submit.prevent="submitAppointmentForm">
          <CardBoxComponentTitle title="Create Appointment">
            <BaseButton :icon="mdiClose" color="whiteDark" small rounded-full
              @click.prevent="createAppointmentModal = false" />
          </CardBoxComponentTitle>
          <BaseDivider />
          <FormField label="Scheduled Date and Time">
            <FormControl v-model="createAppointmentForm.scheduled_date" type="datetime-local" required />
          </FormField>

          <FormField label="Patient Email" v-has-role="['doctor']">
            <FormControl v-model="createAppointmentForm.on_behalf_of" type="email" placeholder="Patient email"
              required />
          </FormField>

          <FormField label="Reason" help="Reason for appointment.">
            <FormControl v-model="createAppointmentForm.reason" type="textarea" required />
          </FormField>


          <template #footer>
            <BaseButtons>
              <BaseButton type="submit" label="Submit" color="info" />
            </BaseButtons>
          </template>
        </CardBox>

      </BaseModal>

      <BaseButton class="mb-5" color="success" label="Book Appointment" @click="createAppointmentModal = true"
        v-has-role="['doctor', 'patient']" />

      <div class="flex justify-end items-center gap-2">

        <FormField label="From:">
          <FormControl v-model="queryParams.params.date_from" type="datetime-local" />
        </FormField>
        <FormField label="To:">
          <FormControl v-model="queryParams.params.date_to" type="datetime-local" />
        </FormField>
        <FormControl class="-mb-2" v-model="queryParams.params.status" :options="statusOptions" />
        <BaseButton class="-mb-2" @click="fetchAppointments" color="info" label="Filter" />

      </div>

      <CardBox has-table>
        <TableAppointments v-if="hasAppointments" :items="appointments.data"
          @refresh-apppointment="fetchAppointments" />
        <CardBoxComponentEmpty v-else />
      </CardBox>

    </SectionMain>
  </LayoutAuthenticated>
</template>
