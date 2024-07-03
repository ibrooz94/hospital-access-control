import { mdiLogout, mdiThemeLightDark } from '@mdi/js'

export default [
  {
    isCurrentUser: true,
    label: 'My Profile',
    to: '/profile'
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
