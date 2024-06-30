import { mdiMonitor, mdiViewList } from '@mdi/js'

export default [
  {
    to: '/appointments',
    icon: mdiMonitor,
    label: 'Appointments',
    meta: ['patient', 'doctor']
  },
  {
    label: 'Visit Management',
    icon: mdiViewList,
    menu: [
      {
        label: 'New Visit',
        to: '/newvisit',
        meta: ['doctor', 'nurse', 'labtech']
      },
      {
        label: 'V',
        to: '/vital',
        meta: ['nurse', 'doctor']
      },
      {
        label: 'LabTests',
        to: '/labtest',
        meta: ['labtech']
      }
    ]
  }
]
