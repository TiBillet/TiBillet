<!--inspiré de card4 : https://demos.creative-tim.com/now-ui-design-system-pro/sections/page-sections/general-cards.html-->
<template>
  <div class="card test-card-event" data-animation="true">
    <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
      <a class="d-block">
        <img v-if="event.categorie === 'CARDE_CREATE'" class="img-fluid shadow border-radius-lg" :src="imgCreateEvent" loading="lazy"
          alt="Image de l'évènement !" />
        <img v-else class="img-fluid shadow border-radius-lg" :src="event.img_variations.crop" loading="lazy"
          alt="Image de l'évènement !" />
      </a>
    </div>

    <div class="card-body">

      <span class="card-title mt-3 h5 d-block text-dark">
        {{ event.categorie === 'CARDE_CREATE' ? "Créer votre évènement" : event.name }}
      </span>

      <p class="text-dark">
        {{ event.categorie === 'CARDE_CREATE' ? "Maintenat" : formateDate(event.datetime) }}

        <span class="text-primary text-uppercase text-sm font-weight-bold tibillet-text-primary">
          <span v-for="(produit, index) in event.products" :key="index">
            <span v-if="produit.categorie_article === 'B'">
              <span v-for="price in produit.prices" :key="produit.uuid">
                - {{ price.prix }}€
              </span>
            </span>
            <span v-if="produit.categorie_article === 'F'">
              <span v-for="price in produit.prices" :key="produit.uuid">
                - ENTRÉE LIBRE
              </span>
            </span>
          </span>
        </span>
      </p>

      <p class="card-description mb-4" v-if="event.short_description !== null">
        {{ event.short_description }}
      </p>
      <p class="card-description mb-4" v-if="event.short_description === null && event.artists[0] !== undefined">
        {{ event.artists[0].configuration.short_description }}
      </p>

      <div v-if="event.categorie === 'CARDE_CREATE'" class="btn btn-outline-primary tibillet-outline-primary btn-sm"
        @click="$router.push({ path: '/create_event'})"
        role="button" aria-label="Créer un évènement">
        Valider
      </div>
      <div v-else class="btn btn-outline-primary tibillet-outline-primary btn-sm"
        @click="$router.push({ path: '/event/' + event.slug, query: { url: event.url, categorie: place.categorie } })"
        role="button" :aria-label="`Réserver ${event.slug}`">
        {{ event.products.length === 0 ? "Informations" : "Réserver" }}
      </div>

    </div>
  </div>
</template>

<script setup>
// image pour la carte de création d'évènements
import imgCreateEvent from "../assets/img/createEvent.jpg"

const props = defineProps({
  event: Object,
  place: Object
})

function formateDate(dateString) {
  const date = new Date(dateString)
  return `${date.toLocaleDateString()} - ${date.toLocaleTimeString()}`
}
</script>

<style></style>