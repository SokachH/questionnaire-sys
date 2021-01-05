import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/Login'
import Base from '@/components/Base'
import Index from '@/components/Index'
import Register from '@/components/Register'
import HomeH from '@/components/HomeH'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Base',
      component: Base,
      children: [
        {
          path: '/',
          name: 'Index',
          component: Index
        },
        {
          path: 'index',
          name: 'Index',
          component: Index
        },
        {
          path: 'login',
          name: 'Login',
          component: Login
        },
        {
          path: 'register',
          name: 'Register',
          component: Register
        },
        {
          path: 'home',
          name: 'HomeH',
          component: HomeH
        }
      ]
    },
    // {
    //   path: '/login',
    //   name: 'Login',
    //   component: Login
    // }
  ]
})
