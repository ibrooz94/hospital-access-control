<script setup>
import { mdiClose, mdiLogout } from '@mdi/js'
import AsideMenuList from '@/components/AsideMenuList.vue'
import AsideMenuItem from './AsideMenuItem.vue';
import BaseIcon from '@/components/BaseIcon.vue'
import { computed } from 'vue';

defineProps({
  menu: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['menu-click', 'aside-lg-close-click'])

const logoutItem = computed(() => ({
  label: 'Logout',
  icon: mdiLogout,
  color: 'info',
  isLogout: true
}))


const menuClick = (event, item) => {
  emit('menu-click', event, item)
}

const asideLgCloseClick = (event) => {
  emit('aside-lg-close-click', event)
}
</script>

<template>
  <aside id="aside"
    class="lg:py-2 lg:pl-2 lg:w-72 w-60 fixed flex z-40 top-0 h-screen transition-position overflow-hidden">
    <div class="aside lg:rounded-2xl flex-1 flex flex-col overflow-hidden bg-neutral-50 dark:bg-slate-900">
      <div class="aside-brand flex flex-col  h-14 items-center justify-between dark:bg-slate-900">
        <!-- flex-row -->
        <div class="text-center flex-1 mt-10 lg:text-left lg:pl-6 xl:text-center xl:pl-0">
          <b class="font-black">Hospital Access Control</b>
        </div>
        <button class="absolute hidden lg:inline-block xl:hidden p-3" @click.prevent="asideLgCloseClick">
          <BaseIcon :path="mdiClose" size="24" />
        </button>
      </div>
      <div class="flex-1 overflow-y-auto overflow-x-hidden aside-scrollbars dark:aside-scrollbars-[slate] mt-10">
        <AsideMenuList :menu="menu" @menu-click="menuClick" />
      </div>
      <ul>
        <AsideMenuItem :item="logoutItem" @menu-click="menuClick" />
      </ul>
    </div>
  </aside>
</template>
