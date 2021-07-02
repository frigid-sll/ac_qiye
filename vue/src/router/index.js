import Vue from 'vue'
import Router from 'vue-router'
import ac_content from '@/components/ac_content'
import relative from '@/components/relative'
import talk from '@/components/talk'
import health from '@/components/health'
import customer from '@/components/customer'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ac_content',
      component: ac_content
    },
    {
      path: '/relative',
      name: 'relative',
      component: relative
    },
    {
      path: '/talk',
      name: 'talk',
      component: talk
    },
    {
      path: '/health',
      name: 'health',
      component: health
    },
    {
      path: '/customer',
      name: 'customer',
      component: customer
    }
  ]
})
