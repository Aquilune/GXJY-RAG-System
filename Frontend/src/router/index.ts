import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArbitrageView from '../views/ArbitrageView.vue'
import FilterView from '../views/FilterView.vue'
import TrendView from '../views/TrendView.vue'
import MapView from '../views/MapView.vue'
import SearchView from '../views/SearchView.vue'
import HelperView from '../views/HelperView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/arbitrage',
      name: 'arbitrage',
      component: ArbitrageView,
    },
    {
      path: '/filter',
      name: 'filter',
      component: FilterView,
    },
    {
      path: '/trend',
      name: 'trend',
      component: TrendView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
    },
    {
      path: '/helper',
      name: 'helper',
      component: HelperView,
    },
  ],
})

export default router
