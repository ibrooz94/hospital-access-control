<script setup>
import { computed, ref, reactive, onMounted } from 'vue'
import {
    mdiChartTimelineVariant,
    mdiClose
} from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import BaseModal from '@/components/BaseModal.vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionTitleLine from '@/components/SectionTitleLine.vue'
import CardBoxComponentEmpty from '@/components/CardBoxComponentEmpty.vue'
import CardBoxComponentTitle from '@/components/CardBoxComponentTitle.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import BaseDivider from '@/components/BaseDivider.vue'
import { API } from '@/services'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import TableLabTest from '@/components/tables/TableLabTest.vue'
import TableVital from '@/components/tables/TableVital.vue'

import SectionTitle from '@/components/SectionTitle.vue'

const toast = useToast()
const route = useRoute()

// watch(
//   () => route.params.id,
//   (newId, oldId) => {
//     // react to route changes...
//   }
// )

const visit = ref(null)
const vitals = ref(null)
const labtests = ref(null)

const createVitalModal = ref(false)
const createVitalForm = reactive({
    temperature: "",
    blood_pressure: "",
})

const createLabTestModal = ref(false)
const createLabTestForm = reactive({
    lab_type: "",
    result: "",
    note: ""
})



const fetchVisit = async () => {
    console.log(route.params.visitId)
    try {
        visit.value = await API.visit.get(route.params.visitId)
        vitals.value = visit.value.data.vitals.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());
        labtests.value = visit.value.data.labtests.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());

    } catch (err) {
        console.error("Error fetching apppintments: ", err.message)
    }
}

const submitVitalForm = async () => {
    try {
        await API.vital.createByVisit(route.params.visitId, createVitalForm)
        createVitalModal.value = false
        toast.success("Vital created")
        fetchVisit()
    } catch (err) {
        createVitalModal.value = false
        console.error("Error creating Vital", err.message)
    }
}

const submitLabTestForm = async () => {
    try {
        await API.labtest.createByVisit(route.params.visitId, createLabTestForm)
        createLabTestModal.value = false
        toast.success("Labtest created!")
        fetchVisit()

    } catch (err) {
        createVitalModal.value = false
        console.error("Error creating LabTest")
    }

}


onMounted(async () => {
    await fetchVisit();
})

const hasVitals = computed(() => visit.value?.data.vitals.length > 0);
const hasLabTests = computed(() => visit.value?.data.labtests.length > 0);



</script>

<template>
    <LayoutAuthenticated>
        <SectionMain>
            <!-- VITAL MODAL -->
            <BaseModal v-model="createVitalModal">
                <CardBox v-show="createVitalModal" class="shadow-lg max-h-modal w-10/12 z-50" is-modal is-form
                    @submit.prevent="submitVitalForm">
                    <CardBoxComponentTitle title="Create Vital">
                        <BaseButton :icon="mdiClose" color="whiteDark" small rounded-full
                            @click.prevent="createVitalModal = false" />
                    </CardBoxComponentTitle>
                    <BaseDivider />
                    <FormField label="Temperature">
                        <FormControl v-model="createVitalForm.temperature" type="text" required />
                    </FormField>

                    <FormField label="Blood Pressure">
                        <FormControl v-model="createVitalForm.blood_pressure" type="text" required />
                    </FormField>

                    <template #footer>
                        <BaseButtons>
                            <BaseButton type="submit" label="Submit" color="info" />
                        </BaseButtons>
                    </template>
                </CardBox>

            </BaseModal>

            <!-- LABTEST MODAL -->
            <BaseModal v-model="createLabTestModal">
                <CardBox v-show="createLabTestModal" class="shadow-lg max-h-modal w-10/12 z-50" is-modal is-form
                    @submit.prevent="submitLabTestForm">
                    <CardBoxComponentTitle title="Create LabTest">
                        <BaseButton :icon="mdiClose" color="whiteDark" small rounded-full
                            @click.prevent="createLabTestModal = false" />
                    </CardBoxComponentTitle>
                    <BaseDivider />
                    <FormField label="Lab Type">
                        <FormControl v-model="createLabTestForm.lab_type" type="text" required />
                    </FormField>

                    <FormField label="Result">
                        <FormControl v-model="createLabTestForm.result" type="text" required />
                    </FormField>

                    <FormField label="Note">
                        <FormControl v-model="createLabTestForm.note" type="text" />
                    </FormField>

                    <template #footer>
                        <BaseButtons>
                            <BaseButton type="submit" label="Submit" color="info" />
                        </BaseButtons>
                    </template>
                </CardBox>

            </BaseModal>

            <SectionTitle first>
                Visit
            </SectionTitle>
            <FormField label="Patient">
                <FormControl v-if="visit" v-model="visit.data.patient.email" type="text" disabled />
            </FormField>



            <SectionTitleLine :icon="mdiChartTimelineVariant" title="Vitals" main></SectionTitleLine>
            <BaseButton class="mb-5" color="success" label="New Vital" @click="createVitalModal = true"
                v-has-role="['nurse']" />
            <CardBox has-table>
                <TableVital v-if="hasVitals" :items="visit.data.vitals" />
                <CardBoxComponentEmpty v-else />
            </CardBox>

            <BaseDivider />



            <SectionTitleLine :icon="mdiChartTimelineVariant" title="Lab Tests" main></SectionTitleLine>
            <BaseButton class="mb-5" color="success" label="New Labtest" @click="createLabTestModal = true"
                v-has-role="['labtech']" />
            <CardBox has-table>
                <TableLabTest v-if="hasLabTests" :items="labtests" />
                <CardBoxComponentEmpty v-else />
            </CardBox>

        </SectionMain>
    </LayoutAuthenticated>
</template>
