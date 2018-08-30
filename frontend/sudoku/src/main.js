import Vue from "vue";
import VueResource from "vue-resource";
import VueRouter from "vue-router";

import App from "./App.vue";
import Hiscores from "./Hiscores.vue";
import Login from "./Login.vue";
import Play from "./Play.vue";
import Signup from "./Signup.vue";
import Solve from "./Solve.vue";
import Users from "./Users.vue";

Vue.use(VueRouter);
Vue.use(VueResource);

// Vue.http.options.emulateJSON = true;

const routes = [
    {path : "/sudoku", component : Play},
    {path : "/sudoku/play", component : Play},
    {path : "/sudoku/solve", component : Solve},
    {path : "/sudoku/hiscores", component : Hiscores},
    {path : "/sudoku/signup", component : Signup},
    {path : "/sudoku/login", component : Login}
];

const router = new VueRouter({routes : routes, mode : "history"});

new Vue({el : "#app", router : router, render : h => h(App)});
