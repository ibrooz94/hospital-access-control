import './css/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import { useDarkModeStore } from './stores/darkMode'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// Init Pinia
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// Create Vue app
const app = createApp(App)
app.use(router)
app.use(pinia)
app.use(Toast)

app.mount('#app')

// Dark mode
const darkModeStore = useDarkModeStore(pinia)

if (
  (!localStorage['darkMode'] && window.matchMedia('(prefers-color-scheme: dark)').matches) ||
  darkModeStore.isEnabled == true
) {
  darkModeStore.set(true)
} else {
  darkModeStore.set(false)
}

// Default title tag
const defaultDocumentTitle = 'Hospital Access Control'

// Set document title from route meta
router.afterEach((to) => {
  document.title = to.meta?.title
    ? `${to.meta.title} — ${defaultDocumentTitle}`
    : defaultDocumentTitle
})
