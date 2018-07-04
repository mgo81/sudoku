<template>
    <div>
        <form id="login-form" @submit.prevent="processForm">
            <div class="form-group">
                <label for="usr">Username:</label>
                <input type="text" class="form-control" id="usr" v-model="username" maxlength="50" v-bind:class="{'is-invalid': trySubmit && missingUName()}">
                <div class="invalid-feedback">Required</div>
            </div>
            <div class="form-group">
                <label for="pwd">Password:</label>
                <input type="password" class="form-control" id="pwd" v-model="password" maxlength="50" v-bind:class="{'is-invalid': trySubmit && missingPassword()}">
                <div class="invalid-feedback">Required</div>
            </div>          
            <div class="form-group">
                <button type="submit" class="btn btn-primary">Signup</button>
            </div>
            <div v-if="alerts" class="alert alert-danger" role="alert">
                Username and Password doesn't match
            </div>
        </form>
    </div>
</template>

<script>
import Cookies from "js-cookie";
import Users from "./users.js";
export default {
  data() {
    return {
      users: Users,
      token: "",
      id: "",
      username: "",
      password: "",
      trySubmit: false,
      alerts: false
    };
  },
  mounted: function() {
    if (this.users.token || Cookies.get("token")) {
      this.$router.push("/");
    }
  },
  methods: {
    missingUName: function() {
      return this.username === "";
    },
    missingPassword: function() {
      return this.password === "";
    },
    processForm: function(event) {
      this.trySubmit = true;
      if (this.missingUName() || this.missingPassword()) {
        event.preventDefault();
      } else {
        this.$http
          .post("http://localhost:5000/api/v1/user/login", {
            username: this.username,
            password: this.password
          })
          .then(function(response) {
            this.token = response.data.data[0].user_token;
            this.id = response.data.data[0].user_id;
            Cookies.set("token", this.token);
            Cookies.set("id", this.id);
            this.users.token = this.token;
            this.users.id = this.id;
            this.$router.push("/");
          })
          .catch(function(error) {
            this.alerts = true;
          });
      }
    }
  }
};
</script>