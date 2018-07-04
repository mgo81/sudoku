<template>
    <div id="app">
        <div class="header">
            <div class="container">
                <div class="row">
                    <h1>Sudoku</h1>
                </div>
                <div class="row">
                    <div class="col-sm-6">
                        <ul>
                            <div class="nav">
                                <li class="nav-item"><a class="nav-link" @click="$router.push('/play')">Play</a></li>
                                <li class="nav-item"><a class="nav-link" @click="$router.push('/solve')">Solver</a></li>
                                <li class="nav-item"><a class="nav-link" @click="$router.push('/hiscores')">Hiscores</a></li>
                            </div>
                        </ul>
                    </div>
                    <div class="col-sm-6">
                        <ul>
                            <div class="nav" style="float: right">
                                <li v-if="!users.token" class="nav-item"><a class="nav-link" @click="$router.push('/login')">Login</a></li>
                                <li v-if="!users.token" class="nav-item"><a class="nav-link" @click="$router.push('/signup')">Signup</a></li>
                                <li v-if="users.token" class="nav-item"><a class="nav-link" v-on:click="logOut" @click="$router.push('/')">Logout</a></li>
                            </div>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-fluid">

            <router-view>
            </router-view>
        </div>
    </div>
</template>

<script>
import Cookies from "js-cookie";
import Users from "./users.js";
export default {
  data() {
    return {
      users: Users,
      tokenTrue: false
    };
  },
  mounted: function() {
    if (Cookies.get("token")) {
      this.users.token = Cookies.get("token");
      this.users.id = Cookies.get("id");
    }
  },
  methods: {
    logOut: function() {
      this.$http
        .post(
          "http://localhost:5000/api/v1/user/logout",
          {},
          {
            headers: { "X-Authorization": Cookies.get("token") }
          }
        )
        .then(function() {
          Cookies.remove("token");
          Cookies.remove("id");
          this.users.token = null;
          this.users.id = null;
        });
    }
  }
};
</script>