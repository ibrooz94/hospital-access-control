import { mdiAccount, mdiEmail, mdiLogout, mdiThemeLightDark } from '@mdi/js'

export default [
  {
    isCurrentUser: true,
    menu: [
      {
        icon: mdiAccount,
        label: 'My Profile',
        to: '/profile'
      },
      {
        icon: mdiEmail,
        label: 'Messages'
      }
    ]
  },
  {
    icon: mdiThemeLightDark,
    label: 'Light/Dark',
    isDesktopNoLabel: true,
    isToggleLightDark: true
  },
  {
    icon: mdiLogout,
    label: 'Log out',
    isDesktopNoLabel: true,
    isLogout: true
  }
]
