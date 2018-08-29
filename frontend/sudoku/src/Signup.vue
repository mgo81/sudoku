<template>
    <div>
        <form id="signup-form" @submit.prevent="processForm">
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
                <label for="cpwd">Confirm Password:</label>
                <input type="password" class="form-control" id="cpwd" v-model="confirmPassword" maxlength="50" v-bind:class="{'is-invalid': trySubmit && missingCPassword()}">
                <div class="invalid-feedback">Required</div>
            </div>            
            <div class="form-group">
                <button type="submit" class="btn btn-primary">Signup</button>
            </div>
            
            <div v-if="alertsU" class="alert alert-danger" role="alert">
                Username already taken
            </div>
            <div v-if="alertsP" class="alert alert-danger" role="alert">
                Passwords don't match
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
      confirmPassword: "",
      trySubmit: false,
      alertsU: false,
      alertsP: false
    };
  },
  mounted: function() {
    console.log(this.users.token);
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
    missingCPassword: function() {
      return this.confirmPassword === "";
    },
    samePassword: function() {
      return this.password != this.confirmPassword;
    },
    processForm: function(event) {
      this.trySubmit = true;
      if (this.samePassword()) {
        this.alertsP = true;
        event.preventDefault();
      }
      if (
        this.missingUName() ||
        this.missingPassword() ||
        this.missingCPassword() ||
        this.samePassword()
      ) {
        event.preventDefault();
      } else {
        this.$http
          .post("http://rafaelgoesmann:9000/api/v1/user/signup", {
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
            console.log(Users.token);
            this.$router.push("/");
          })
          .catch(function(error) {
            this.alertsU = true;
          });
      }
    }
  }
};
</script>