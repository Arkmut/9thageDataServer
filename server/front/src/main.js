import Vue from 'vue'
import VueCookies from 'vue-cookies'
import VueRouter from 'vue-router'
import axios from 'axios';
import { ValidationProvider } from 'vee-validate';

import App from './App.vue'
import ArmyEditor from './components/ArmyEditor.vue'

//router
const routes = [
  { path: '/', component: App },
  { path: '/army/:name/:version', component: ArmyEditor, props: route => ({ ...route.params }) },
]
const router = new VueRouter({
  mode: 'history',
  routes, // short for `routes: routes`
})

Vue.prototype.$http = axios;
Vue.prototype.$router = router;
Vue.config.productionTip = false
Vue.use(VueCookies, { expires: '1d'});
Vue.use(VueRouter);
Vue.component('ValidationProvider', ValidationProvider);



new Vue({
router,
  render: h => h(App),
}).$mount('#app')
