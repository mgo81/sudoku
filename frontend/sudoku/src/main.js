import Vue from "vue";
import App from "./App.vue";
import Play from "./Play.vue";
import Solve from "./Solve.vue";
import Hiscores from "./Hiscores.vue";
import Users from "./Users.vue";
import Signup from "./Signup.vue";
import Login from "./Login.vue";

import VueRouter from "vue-router";
import VueResource from "vue-resource";

Vue.use(VueRouter);
Vue.use(VueResource);

//Vue.http.options.emulateJSON = true;

const routes = [
  {
    path: "/",
    component: Users
  },
  {
    path: "/play",
    component: Play
  },
  {
    path: "/solve",
    component: Solve
  },
  {
    path: "/hiscores",
    component: Hiscores
  },
  {
    path: "/signup",
    component: Signup
  },
  {
    path: "/login",
    component: Login
  }
];

const router = new VueRouter({
  routes: routes,
  mode: "history"
});

new Vue({
  el: "#app",
  router: router,
  render: h => h(App)
});
