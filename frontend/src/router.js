import Vue from 'vue'
import Router from 'vue-router'
import Room from './components/Room.vue'
import Play from './components/Play.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'room',
      component: Room
    },
    {
      path: '/:room_name',
      name: 'play',
      component: Play
    }
  ]
})
