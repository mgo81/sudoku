<template>
    <div>
        <form id="puzzle-form" @submit.prevent="processForm">
            <table>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>
                <tbody v-for="(tbody, tindex) in puzzle" v-bind:key="tindex">
                    <tr v-for="(row, rindex) in tbody" v-bind:key="rindex">
                        <td v-for="(cell, cindex) in row" v-bind:key="cindex">
                            <input v-if="!check[tindex][rindex][cindex]" v-model.number="puzzle[tindex][rindex][cindex]" type="text" maxlength="1" pattern="[1-9]" style="width: 64px; height: 64px; text-align: center; color: blue;">
                            <div v-else><strong>{{cell}}</strong></div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="alerts" class="alert alert-danger" role="alert" style="margin: 0 auto; width: 540px;">
                Cannot generate solution
            </div>
            <div v-if="!solved" class="form-group" style="text-align: center;">
                <button type="submit" class="btn btn-primary">Solve</button>
            </div>

        </form>
        <div v-if="solved" style="text-align: center;">
            <button type="submit" class="btn btn-primary" v-on:click="getBoard()">Solve another</button>
        </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      puzzle: [],
      check: [],
      alerts: false,
      solved: false
    };
  },
  mounted: function() {
    this.getBoard();
  },
  methods: {
    getBoard: function() {
      this.solved = false;
      this.alerts = false;
      this.puzzle = [
        [
          ["", "", "", "", "", "", "", "", ""],
          ["", "", "", "", "", "", "", "", ""],
          ["", "", "", "", "", "", "", "", ""]
        ],
        [
          ["", "", "", "", "", "", "", "", ""],
          ["", "", "", "", "", "", "", "", ""],
          ["", "", "", "", "", "", "", "", ""]
        ],
        [
          ["", "", "", "", "", "", "", "", ""],
          ["", "", "", "", "", "", "", "", ""],
          ["", "", "", "", "", "", "", "", ""]
        ]
      ];
      this.check = JSON.parse(JSON.stringify(this.puzzle));
    },
    processForm: function() {
      this.alerts = false;
      let temp = [];
      let i = 0;
      for (let tbod of this.puzzle) {
        for (let row of tbod) {
          temp.push(row);
        }
      }

      this.$http
        .post("https://sudoku.rafaelgoesmann.com:9000/api/v1/puzzle/solution", {
          puzzle: temp
        })
        .then(function(response) {
          console.log(response.data.data.length);
          if (!response.data.data.length) {
            this.alerts = true;
          } else {
            let i = response.data.data;
            this.puzzle = [
              [i[0], i[1], i[2]],
              [i[3], i[4], i[5]],
              [i[6], i[7], i[8]]
            ];
            this.solved = true;

            this.check = JSON.parse(JSON.stringify(this.puzzle));
          }
        });
    }
  }
};
</script>