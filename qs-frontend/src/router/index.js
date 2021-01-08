import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/Login'
import Base from '@/components/Base'
import Index from '@/components/Index'
import Register from '@/components/Register'
// import HomeH from '@/components/HomeH'
import Home from '@/components/Home'
import Display from '@/components/Display'
import TempDisplay from '@/components/TempDisplay'
import ThankYou from '@/components/ThankYou'
// import testLogin from '@/components/testLogin'
import ResetPass from '@/components/ResetPass'
import Count from '@/components/Count'
import Home_bak from '@/components/Home_bak'
import activeInput from '@/components/activeInput'
import backhome from '@/components/backhome'
import Login_admin from '@/components/Login_admin'
import Base_admin from '@/components/Base_admin'
import temp_login from '@/components/temp_login'

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
          name: 'Home',
          component: Home
        },
        {
          path: 'resetpass',
          name: 'ResetPass',
          component: ResetPass
        }
      ]
    },
    {
      path: '/display/:id',
      name: 'Display',
      component: Display
    },
    {
      path: '/tempdisplay/:id',
      name: 'TempDisplay',
      component: TempDisplay
    },
    {
      path: '/thankyou',
      name: 'ThankYou',
      component: ThankYou
    },
    {
      path: '/admin',
      name: 'BaseAdmin',
      component: Base_admin,
      children: [
        // {
        //   path: '/',
        //   name: 'adminlogin',
        //   component: Login_admin
        // },
        // {
        //   path: '/',
        //   name: 'adminlogin',
        //   component: temp_login
        // },
        {
          path: '/adminlogin',
          name: 'adminlogin',
          component: Login_admin
        },
        // {
        //   path: 'adminlogin',
        //   name: 'adminlogin',
        //   component: Login_admin
        // },
        {
          path: '/backhome',
          name: 'backhome',
          component: backhome
        },
      ]
    },
    {
      path: '/testc',
      name: 'testc',
      component: Count
    },
    {
      path: '/testh',
      name: 'testh',
      component: Home_bak
    },
    {
      path: '/testa',
      name: 'testa',
      component: activeInput
    },
  ]
})
