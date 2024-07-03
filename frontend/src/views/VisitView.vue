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
import TableVisit from '@/components/tables/TableVisits.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseDivider from '@/components/BaseDivider.vue'
import { API } from '@/services'
import { useToast } from 'vue-toastification'

const toast = useToast()

const visits = ref(null)
const queryParams = reactive({
  params: {
    visit_status: null,
    sort: "-updated_at"
  }
});
const createVisitForm = reactive({
  reason_for_visit: "",
  visit_status: null,
})

const statusOptions = [
  { value: null, label: "Status" },
  { value: "admitted", label: "Admitted" },
  { value: "discharged", label: "Discharged" },
  { value: "checked_in", label: "Checked In" },
  { value: "checked_out", label: "Checked Out" },
]
const visitTypeOptions = [
  { value: "checked_in", label: "Admission" },
  { value: "admitted", label: "Consultation" },
]

const fetchVisits = async () => {
  try {
    visits.value = await API.visit.list(queryParams)
  } catch (err) {
    console.error("Error fetching apppintments: ", err.message)
  }
}

const submitAppointmentForm = async () => {
  try {
    await API.visit.create(createVisitForm)
    createVisitModal.value = false
    toast.success("Appointment created")

  } catch (err) {
    createVisitModal.value = false
    console.error("Error creating appointment", err.message)
  }
}

onMounted(async () => {
  await fetchVisits();
})

const hasVisits = computed(() => visits.value?.data.length > 0);
const admittedCount = computed(() => visits.value?.data.filter(visit => visit.visit_status === 'checked_in' || visit.visit_status === 'admitted').length || 0);

const createVisitModal = ref(false)

</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>
      <SectionTitleLine :icon="mdiChartTimelineVariant" title="Visits" main>
      </SectionTitleLine>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
        <!-- <CardBoxWidget color="text-blue-500" :icon="mdiAccountMultiple" :number="bookedCount" label="Booked" /> -->
        <CardBoxWidget color="text-yellow-500" :icon="mdiAccountMultiple" :number="admittedCount" label="Pending" />
      </div>

      <BaseModal v-model="createVisitModal">
        <CardBox v-show="createVisitModal" class="shadow-lg max-h-modal w-10/12 z-50" is-modal is-form
          @submit.prevent="submitAppointmentForm">
          <CardBoxComponentTitle title="Create New Visit">
            <BaseButton :icon="mdiClose" color="whiteDark" small rounded-full
              @click.prevent="createVisitModal = false" />
          </CardBoxComponentTitle>
          <BaseDivider />
          <FormField label="Visit Type">
            <FormControl v-model="createVisitForm.visit_status" :options="visitTypeOptions" required />
          </FormField>

          <FormField label="Reason" help="Reason for Visit.">
            <FormControl v-model="createVisitForm.reason" type="textarea" required />
          </FormField>

          <template #footer>
            <BaseButtons>
              <BaseButton type="submit" label="Submit" color="info" />
            </BaseButtons>
          </template>
        </CardBox>

      </BaseModal>

      <BaseButton class="mb-5" color="success" label="New Visit" @click="createVisitModal = true"
        v-has-role="['doctor', 'nurse', 'labtech']" />

      <div class="flex justify-end items-center gap-2 mb-3">
        <FormField>

          <FormControl v-model="queryParams.params.visit_status" :options="statusOptions" />
          <BaseButton @click="fetchVisits" color="info" label="Filter" />
        </FormField>

      </div>

      <CardBox has-table>
        <TableVisit v-if="hasVisits" :items="visits.data" />
        <CardBoxComponentEmpty v-else />
      </CardBox>

    </SectionMain>
  </LayoutAuthenticated>
</template>
