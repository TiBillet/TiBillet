// gère les routes(pages)
import {createRouter, createWebHistory} from 'vue-router'

// store
import {useLocalStore} from '@/stores/local'
import {useAllStore} from '@/stores/all'

const domain = `${location.protocol}//${location.host}`

const routes = [
   {
    // 404, route interceptée
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: {}
  },
  {
    // route interceptée
    path: '/stripe/return/:id',
    name: 'StripeReturn',
    component: {}
  },
  {
    path: '/event/:slug',
    name: 'Event',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "Event" */ '../views/Event.vue'),
    // chargement synchrone des données lieu et évènements avant d'entrer dans la vue
    /*
    async beforeEnter(to, from) {
      await loadEventBySlug(to.params.slug)
    }
     */
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // always scroll to top
    return {
      top: 0,
      behavior: 'smooth'
    }
  }
})


router.beforeEach((to, from, next) => {
  // traitement de la redirection si interception
  let redirection = false
  let nouvelleRoute = '/'
  if (from.name !== undefined) {
    nouvelleRoute = from.path
  }

  // intercepte la route "NotFound" et redirige sur le wiki tibillet
  if (to.name === "NotFound") {
    console.log(`redirection stopée --> router/index.js, route 'NotFound'`)
    // window.location = "https://wiki.tibillet.re/"
  }


  // intercepte retour de stripe
  if (to.name === "StripeReturn") {
    // console.log('--------------------------------------------------------------------------------------------------')
    // console.log('Interception "StripeReturn" !')
    // console.log('to =', to)
    const uuidStripe = to.params.id
    // console.log('uuidStripe =', uuidStripe)
    if (uuidStripe !== undefined) {
      const {postStripeReturn} = useLocalStore()
      postStripeReturn(uuidStripe)
    } else {
      emitter.emit('message', {
        tmp: 6,
        typeMsg: 'danger',
        contenu: `Retour stipe, erreur: id indéfini !`
      })
    }
    nouvelleRoute = '/'
    redirection = true
  }

  if (redirection === true) {

    next({
      path: nouvelleRoute,
      replace: true
    })
  } else {
    next()
  }

  //   console.log('from =', from)
  // console.log('to =', to)
  useAllStore().routeName = to.name

})


export default router
