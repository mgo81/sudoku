<template>
    <div>  
        <div class="row" style="width: 630px; margin: 0 auto;">
            <div class="col-sm-5">
                <label for="diffselect" style="color: white;">Difficulty</label>
                <select v-model="difficulty" class="form-control" id="diffselect">
                    <option v-for="diff in difficulties" v-bind:key="diff">{{diff.difficulty_name}}</option>
                </select>
            </div>
            <div class="col-sm-2">
                <div class="form-group" style="padding: 0px;">
                    <button v-on:click="getBoard" class="btn btn-primary" style="bottom: 0px; position: absolute;">Generate</button>
                </div>
                <div style="color: white; margin-left: 150px; margin-top: 40px;">{{seconds}}</div> 
            </div>
             
                         
        </div>
        <form id="puzzle-form" @submit.prevent="processForm">
            <table>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>
                <tbody v-for="(tbody, tindex) in puzzle" v-bind:key="tbody">
                    <tr v-for="(row, rindex) in tbody" v-bind:key="row">
                        <td v-for="(cell, cindex) in row" v-bind:key="cell">
                            <input v-if="!check[tindex][rindex][cindex]" v-model.number="puzzle[tindex][rindex][cindex]" type="text" maxlength="1" pattern="[1-9]" style="width: 64px; height: 64px; text-align: center; color: blue;">
                            <div v-else><strong>{{cell}}</strong></div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="alerts" class="alert alert-danger" role="alert" style="margin: 0 auto; width: 540px;">
                Incorrect
            </div>
            <div v-if="alertsGood" class="alert alert-success" role="alert" style="margin: 0 auto; width: 540px;">
                Correct
            </div>
            <div class="form-group" style="text-align: center;">
                <button v-if="generated" type="submit" class="btn btn-primary">Check</button>
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
      puzzle: [],
      check: [],
      alerts: false,
      alertsGood: false,
      difficulty: "easy",
      difficulties: [],
      generated: false,
      seconds: 0,
      allowIncrement: false,
      users: Users
    };
  },
  mounted: function() {
    if (Cookies.get("token")) {
      this.users.token = Cookies.get("token");
      this.users.id = Cookies.get("id");
    }
    this.timer();
    this.getDifficulties();
  },
  methods: {
    getBoard: function() {
      this.alerts = false;
      this.alertsGood = false;
      this.allowIncrement = false;
      this.generated = true;

      this.$http
        .get(
          "http://localhost:9000/api/v1/puzzle/generate?difficulty=" +
            this.difficulty
        )
        .then(function(response) {
          let i = response.data.data;
          this.puzzle = [
            [i[0], i[1], i[2]],
            [i[3], i[4], i[5]],
            [i[6], i[7], i[8]]
          ];

          this.check = JSON.parse(JSON.stringify(this.puzzle));
          this.allowIncrement = true;
          this.seconds = 0;
        });
    },
    getDifficulties: function() {
      this.$http
        .get("http://localhost:9000/api/v1/puzzle/difficulties")
        .then(function(response) {
          this.difficulties = response.data.data;
        });
    },
    processForm: function() {
      let temp = [];
      let i = 0;
      for (let tbod of this.puzzle) {
        for (let row of tbod) {
          temp.push(row);
        }
      }

      this.$http
        .post("http://localhost:9000/api/v1/puzzle/check", {
          puzzle: temp
        })
        .then(function(response) {
          if (response.data.data == false) {
            this.alertsGood = false;
            this.alerts = true;
          } else {
            this.alerts = false;
            this.alertsGood = true;
            this.allowIncrement = false;
            if (Cookies.get("token")) {
              this.$http.post(
                "http://localhost:9000/api/v1/hiscores",
                {
                  difficulty: this.difficulty,
                  score: this.seconds
                },
                {
                  headers: {
                    "Content-Type": "application/json",
                    "X-Authorization": Cookies.get("token")
                  }
                }
              );
            }
          }
          console.log(response.data);
          temp = [];
          i = 0;
        });
    },
    timer() {
      this.seconds = 0;
      setInterval(() => {
        if (this.allowIncrement) {
          this.seconds += 1;
        }

        console.log(this.seconds);
      }, 1000);
    }
  }
};
</script>