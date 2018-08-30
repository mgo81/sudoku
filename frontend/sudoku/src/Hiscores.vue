<template>
    <div>
        <div id="hiscores">
            <form id="hiscore_form" @submit.prevent="getHiscores">
                <div class="row" style="width: 600px;">
                    <div class="col-sm-5">
                        <label for="typeselect" style="color: white;">Type</label>
                        <select v-model="category" class="form-control" id="typeselect">
                            <option>all</option>
                            <option v-if="token || users.token">own</option>
                        </select>
                    </div>
                    <div class="col-sm-5">
                        <label for="diffselect" style="color: white;">Difficulty</label>
                        <select v-model="difficulty" class="form-control" id="diffselect">
                            <option>all</option>
                            <option v-for="diff in difficulties" v-bind:key="diff">{{diff.difficulty_name}}</option>
                        </select>
                    </div>
                    <div class="col-sm-2">
                        <div class="form-group" style="padding: 0px;">
                            <button type="submit" class="btn btn-primary" style="bottom: 0px; position: absolute;">Refresh</button>
                        </div>
                    </div>                    
                </div>
                
            <div id="inner">
                <div class="row">
                    <div class="col-sm-4">
                        <p><strong>Username</strong></p>
                    </div>
                    <div class="col-sm-4">
                        <p><strong>Difficulty</strong></p>
                    </div>
                    <div class="col-sm-4">
                        <p><strong>Time</strong></p>
                    </div>
                </div>
                <div v-for="hiscore in hiscores" class="row">
                    <div class="col-sm-4">
                        <p>{{hiscore.user_name}}</p>
                    </div>
                    <div class="col-sm-4">
                        <p>{{hiscore.difficulty_name}}</p>
                    </div>
                    <div class="col-sm-4">
                        <p>{{hiscore.hiscore_time}}</p>
                    </div>
                </div>                
            </div>
            </form>
        </div>
    </div>
</template>

<script>
import Cookies from "js-cookie";
import Users from "./users.js";
export default {
  data() {
    return {
      difficulties: [],
      token: Cookies.get("token"),
      users: Users,
      category: "all",
      difficulty: "all",
      hiscores: []
    };
  },
  mounted: function() {
    this.getDifficulties();
  },
  methods: {
    getDifficulties: function() {
      this.$http
        .get("https://sudoku.rafaelgoesmann.com/api/v1/puzzle/difficulties")
        .then(function(response) {
          this.difficulties = response.data.data;
          this.getHiscores();
        });
    },
    getHiscores: function() {
      this.$http
        .get(
          "https://sudoku.rafaelgoesmann.com/api/v1/hiscores?category=" +
            this.category +
            "&difficulty=" +
            this.difficulty,

          {
            headers: { "X-Authorization": this.token }
          }
        )
        .then(function(response) {
          this.hiscores = response.data.data;
          console.log(this.hiscores);
          console.log("yeet");
        });
    }
  }
};
</script>