<template>
  <nav id="navbar" class="navbar navbar-expand-lg z-index-3 w-100 navbar-transparent position-fixed">
    <div class="container">
      <!-- lieu -->
      <div class="navbar-brand">
        <router-link to="/" class="navbar-brand d-flex justify-content-between align-items-center">
          <h6 class="m-0 text-white">{{ place.organisation }}</h6>
        </router-link>
      </div>

      <!-- partie droite -->
      <ul class="navbar-nav d-flex flex-row-reverse ms-auto d-block">
        <!-- user -->
        <li v-if="adhesion.status === 'membership' || refreshToken !== ''" class="nav-item dropdown">
          <a class="nav-link d-flex justify-content-between align-items-center dropdown-toggle me-1" href="#"
             id="menuUser"
             role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="fas fa-user me-1" aria-hidden="true"></i>
            <h6 class="m-0 text-white">User</h6>
          </a>
          <!-- menu user -->
          <ul class="dropdown-menu w-100" aria-labelledby="menuUser">
            <!-- déconnexion -->
            <li v-if="refreshToken !== ''">
              <a class="dropdown-item border-radius-md d-flex justify-content-star align-items-center"
                 role="button" @click="disconnect()">
                <i class="fa fa-sign-out text-dark" aria-hidden="true"></i>
                <h6 class="m-0 text-dark">Deconnexion</h6>
              </a>
            </li>
            <!-- assets -->
            <li v-if="infosCardExist() === true">
              <a class="dropdown-item border-radius-md d-flex justify-content-star align-items-center"
                 role="button" @click="showAssets()">
                <i class="fas fa-address-card fa-fw me-1 text-dark" aria-hidden="true"></i>
                <h6 class="m-0 text-dark">Carte</h6>
              </a>
            </li>
            <!-- réservations -->
            <li v-if="infosReservationExist() === true">
              <a class="dropdown-item border-radius-md d-flex justify-content-star align-items-center"
                 role="button" @click="showReservations()">
                <i class="fas fa-address-card fa-fw me-1 text-dark" aria-hidden="true"></i>
                <h6 class="m-0 text-dark">Réservation(s)</h6>
              </a>
            </li>

            <!-- infos adhésion -->
            <li v-if="adhesion.status === 'membership'">
              <a class="dropdown-item border-radius-md d-flex justify-content-star align-items-center"
                 role="button" @click="showAdhesion()">
                <i class="fas fa-address-card fa-fw me-1 text-dark" aria-hidden="true"></i>
                <h6 class="m-0 text-dark">Adhésion</h6>
              </a>
            </li>

          </ul>
        </li>

        <!-- pas de connexion -->
        <li class="nav-item">
          <a v-if="refreshToken === ''" class="nav-link ps-1 d-flex justify-content-between align-items-center"
             role="button"
             data-bs-toggle="modal" data-bs-target="#modal-form-login">
            <i class="fa fa-user-circle-o me-1 text-white" aria-hidden="true"></i>
            <h6 class="m-0 text-white">Se connecter</h6>
          </a>
        </li>

        <!-- pas d'adhésion -->
        <li class="nav-item">
          <a v-if="adhesion.status === ''" class="nav-link ps-1 d-flex justify-content-between align-items-center"
             :title="`Adhérez à l'association '${ place.organisation }'`"
             role="button" data-bs-toggle="modal" data-bs-target="#modal-form-adhesion">
            <i class="fa fa-address-card me-1 text-white" aria-hidden="true"></i>
            <h6 class="m-0 text-white">Adhérez</h6>
          </a>
        </li>

      </ul>

    </div>
  </nav>
</template>

<script setup>
// console.log(' -> Navbar.vue !')

import '../assets/css/google_fonts_family_montserrat_400.700.200.css'

// Nucleo Icons (ui)
import '../assets/css/nucleo-icons.css'

// Font Awesome Free 5.15.4 MIT License
import '../assets/js/kit-fontawesome-42d5adcbca.js'

// bootstrap (ui)
import '../assets/css/bootstrap-5.0.2/bootstrap.min.css'
import '../assets/js/bootstrap-5.0.2/bootstrap.bundle.min.js'

// perfect-scrollbar
import '../assets/css/perfect-scrollbar.css'
import '../assets/js/perfect-scrollbar/perfect-scrollbar.min.js'

// css (ui)
import '../assets/css/now-design-system-pro.min.css'
import '../assets/js/now-design-system-pro.js'

// store
import {storeToRefs} from 'pinia'
import {useAllStore} from '@/stores/all'
import {useLocalStore} from '@/stores/local'

const {place, events, loading, error} = storeToRefs(useAllStore())
const {getPlace} = useAllStore()
const {refreshToken, me, adhesion} = storeToRefs(useLocalStore())
const {infosCardExist, infosReservationExist, getMe, refreshAccessToken} = useLocalStore()

// load place
getPlace()

if (window.accessToken === '' && refreshToken.value !== '') {
  updateAccessToken()
}

async function updateAccessToken() {
  // console.log('-> fonc updateAccessToken !')
  loading.value = true
  await refreshAccessToken(refreshToken.value)
  loading.value = false
}

function disconnect() {
  refreshToken.value = ''
  me.value = {}
  adhesion.value = {
    email: '',
    first_name: '',
    last_name: '',
    phone: null,
    postal_code: null,
    adhesion: '',
    status: ''
  }
}

function dateToFrenchFormat(dateString) {
  const nomMois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
  const dateArray = dateString.split('T')[0].split('-')
  const mois = nomMois[parseInt(dateArray[1])]
  return dateArray[2] + ' ' + mois + ' ' + dateArray[0]
}

function showAdhesion() {
  let contenu = ``
  try {
    console.log('me:', me.value)
    const infos = me.value.cashless
    contenu += `
      <h5>Email : ${infos.email}</h5>
      <h5>Nom : ${infos.name}</h5>
      <h5>Prenom : ${infos.prenom}</h5>
      <h5>Inscription : ${dateToFrenchFormat(infos.date_ajout)}</h5>
      <h5>Echéance : ${dateToFrenchFormat(infos.prochaine_echeance)}</h5>
    `
  } catch (error) {
    console.log('showAdhesion:', error)
    contenu = `<h3>Aucune donnée !</h3>`
  }
  emitter.emit('modalMessage', {
    titre: 'Adhésion',
    dynamic: true,
    scrollable: true,
    contenu: contenu
  })
}

async function updateMe() {
  if (window.accessToken !== '') {
    loading.value = true
    me.value = await getMe(window.accessToken)
    loading.value = false
    return {error: 0}
  }
  return {error: 1, message: 'Access token inconnu !'}
}

async function showAssets() {
  let contenu = ``
  try {
    const actu = await updateMe()
    if (actu.error === 1) {
      throw new Error(message)
    }
    for (const cardKey in me.value.cashless.cards) {
      const card = me.value.cashless.cards[cardKey]
      contenu += `
        <fieldset class="shadow-sm p-3 mb-5 bg-body rounded">
          <legend>
              <h5 class="font-weight-bolder text-info text-gradient align-self-start w-85">Numéro ${card.number}</h5>
          </legend>
          <div class="flex-column">
      `

      // assets
      for (const assetKey1 in card.assets) {
        const monnaie = card.assets[assetKey1]
        contenu += `
          <div class="row">
            <div class="col-8">${monnaie.qty} ${monnaie.monnaie_name}</div>
            <div class="col-4">${dateToFrenchFormat(monnaie.last_date_used)}</div>
          </div>
        `
      }

      contenu += `
          </div>
        </fieldset>
      `
    }
  } catch (error) {
    contenu = `<h3>Aucune donnée !</h3>`
  }

  emitter.emit('modalMessage', {
    titre: 'Carte(s)',
    dynamic: true,
    scrollable: true,
    contenu: contenu
  })
}

async function showReservations() {
  let contenu = ``
  try {
    const actu = await updateMe()
    if (actu.error === 1) {
      throw new Error(message)
    }

    for (const key in me.value.reservations) {
      const reservation = me.value.reservations[key]
      console.log('--> reservation =', reservation)
      const eventFind = events.value.find(evt => evt.uuid === reservation.event)
      console.log('eventFind =', eventFind)

      for (const prodKey in eventFind.products) {
        const prices = eventFind.products[prodKey].prices
        console.log('prices =', prices)
      }

      const eventName = eventFind.name

      contenu += `
        <fieldset class="shadow-sm p-3 mb-5 bg-body rounded">
          <legend>
              <h5 class="font-weight-bolder text-info text-gradient align-self-start w-85"> ${eventName} - ${dateToFrenchFormat(reservation.datetime)}</h5>
          </legend>
          <div class="flex-column">
      `

      for (const ticketKey in reservation.tickets) {
        const ticket = reservation.tickets[ticketKey]
        console.log('ticket = ', ticket)
        contenu += `
          <div class="row">
            <div class="col-8">${ticket.first_name} ${ticket.last_name}</div>
            <div class="col-4">
              <a href="${ticket.pdf_url}" download="ticket-${ticket.first_name}_${ticket.last_name}" class="d-flex flex-row-reverse align-items-center">
                <i class="fa fa-download ms-1" aria-hidden="true"></i>
                <h6 class="m-0 text-dark">Télécharger</h6>
              </a>
            </div>
          </div>
        `
      }

      contenu += `
          </div>
        </fieldset>
      `
    }


  } catch (error) {
    console.log('Rservation, erreur:', error)
    contenu = `<h3>Aucune donnée !</h3>`
  }
  emitter.emit('modalMessage', {
    titre: 'Réservation(s)',
    dynamic: true,
    // xl, lg, sm
    size: 'xl',
    scrollable: true,
    contenu: contenu
  })
}

// menu transparant / non transparant
window.addEventListener("scroll", () => {
  if (document.querySelector('#navbar') !== null) {
    if (scrollY === 0) {
      document.querySelector('#navbar').style.backgroundColor = ''
    } else {
      document.querySelector('#navbar').style.backgroundColor = '#384663'
    }
  }
})

</script>

<style>

</style>