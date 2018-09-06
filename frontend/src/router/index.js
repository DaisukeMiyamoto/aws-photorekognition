import Vue from 'vue'
import Router from 'vue-router'
import PhotoManager from '@/components/PhotoManager'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'root',
      component: PhotoManager
    }
  ]
})
