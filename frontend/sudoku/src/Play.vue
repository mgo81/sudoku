<template>
    <div>
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
            <div class="form-group" style="text-align: center;">
                <button type="submit" class="btn btn-primary">Check</button>
            </div>

        </form>
    </div>
</template>

<script>
export default {
  data() {
    return {
      puzzle: [],
      check: [],
      alerts: false
    };
  },
  mounted: function() {
    this.getBoard();
  },
  methods: {
    getBoard: function() {
      this.$http
        .get("http://localhost:5000/api/v1/puzzle/generate?difficulty=easy")
        .then(function(response) {
          let i = response.data.data;
          this.puzzle = [
            [i[0], i[1], i[2]],
            [i[3], i[4], i[5]],
            [i[6], i[7], i[8]]
          ];

          this.check = JSON.parse(JSON.stringify(this.puzzle));
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
        .post("http://localhost:5000/api/v1/puzzle/check", {
          puzzle: temp
        })
        .then(function(response) {
          if (response.data.data == false) {
            this.alerts = true;
          } else {
            this.alerts = false;
          }
          console.log(response.data);
          temp = [];
          i = 0;
        });
    }
  }
};
</script>