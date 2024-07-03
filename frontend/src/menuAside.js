import { mdiMonitor, mdiViewList } from '@mdi/js'

export default [
  {
    to: '/appointments',
    icon: mdiMonitor,
    label: 'Appointments',
    meta: ['patient', 'doctor']
  },
  {
    to: '/visits',
    icon: mdiViewList,
    label: 'Visits',
    meta: ['doctor', 'nurse', 'labtech']
  }
]
