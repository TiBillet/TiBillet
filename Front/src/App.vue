<template>
  <Loading v-if="loading" />
  <!-- en cours -->
  <Navbar v-if="identitySite && loadingPlace" />
  <Header v-if="identitySite && loadingPlace" />
  <router-view></router-view>
  <ModalMessage />
  <Modallogin />
  <ModalMembershipOwned />
  <ToastContainer />
  <ModalReservationList />
  <ModalOnboard />
  <!--
  <ModalPassword/>
  <ModalCardsList/>

  -->
</template>

<script setup>
// console.log('-> App.vue')
import { ref } from 'vue'

import Plausible from 'plausible-tracker'

// composants
import Loading from "@/components/Loading.vue"
import Navbar from "@/components/Navbar.vue"
import Header from "@/components/Header.vue"
import ModalMessage from "@/components/ModalMessage.vue"
import Modallogin from "@/components/Modallogin.vue"
import ModalMembershipOwned from "@/components/ModalMembershipOwned.vue"
import ToastContainer from "./components/ToastContainer.vue"
import ModalReservationList from "@/components/ModalReservationList.vue"
import ModalOnboard from "@/components/ModalOnboard.vue"


// import ModalPassword from '@/components/ModalPassword.vue'
// import ModalCardsList from '@/components/ModalCardsList.vue'

// store
import { storeToRefs } from 'pinia'
import { useSessionStore } from '@/stores/session'

// font monserrat
import './assets/css/font_Montserrat_Open_Sans_Condensed.css'

// session store
const sessionStore = useSessionStore()
const { identitySite, loading } = storeToRefs(sessionStore)
const { loadPlace } = sessionStore
const loadingPlace = ref(false)

// gestion synchrone du chargement des informations du tenant/lieu/artist/...
async function waitLoadPlace() {
  loadingPlace.value = await loadPlace()
}

waitLoadPlace()

const plausible = Plausible({
  domain: `${window.location.protocol}//${window.location.host}`
})
</script>

<style>
.h-44px {
  height: 44px !important;
}

.l-120px {
  width: 120px;
}

#app {
  --app-color-primary: #f05f3e;
  --app-color-secondary: #0d6efd;
}

.tibillet-outline-primary {
  color: var(--app-color-primary) !important;
  border-color:var(--app-color-primary) !important;
  border: 1px solid var(--app-color-primary) !important;
}

.tibillet-text-primary span {
  color:var(--app-color-primary) !important;
}

.tibillet-bg-primary {
  background-color:var(--app-color-primary) !important;
  color: white !important;
}


.tibillet-bg-secondary {
  background-color: var(--app-color-secondary) !important;
  color: white !important;
}

.tibillet-color-secondary {
  color: var(--app-color-secondary) !important;
}
</style>
