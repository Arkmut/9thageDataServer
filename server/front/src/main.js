import Vue from 'vue'
import VueCookies from 'vue-cookies'
import VueRouter from 'vue-router'
import axios from 'axios';
import { ValidationProvider } from 'vee-validate';

import App from './App.vue'
import ArmyEditor from './components/ArmyEditor.vue'
import LoginView from './components/LoginView.vue'
import LogoutView from './components/LogoutView.vue'


//router
const routes = [
  { path: '/', component: App },
  { path: '/logout', component: LogoutView },
  { path: '/login', component: LoginView },
  { path: '/army/:name/:version', component: ArmyEditor, props: route => ({ ...route.params }) },
]
const router = new VueRouter({
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
