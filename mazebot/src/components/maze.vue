<template>
  <v-container fill-height>
    <v-layout align-center justify-center>
      <v-flex>
        <div class="text-center">
          <v-dialog
            v-model="completeDialog"
            max-width="400px"
            persistent
            ref="dialog"
          >
            <v-card>
              <v-card-title class="headline; justify-center"
                >Congratulations!</v-card-title
              >
              <v-card-text>{{ message }}</v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn @click="newGame">New Game</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <canvas
            v-show="ready"
            ref="canvas"
            :width="width * cols"
            :height="height * rows"
            style="border: 1px solid black; display: block; margin-right: auto; margin-left: auto;"
            @keyup="move"
            tabindex="0"
          >
          </canvas>
          <v-btn @click="newGame" class="btn">{{ btn_message }}</v-btn>
          <v-btn @click="solve" v-if="ready" :disabled="solve_btn" class="btn"
            >I give up..</v-btn
          >
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "maze",
  data() {
    return {
      timer: null,
      solve_btn: false,
      solution: null,
      isFinished: false,
      completed: null,
      completeDialog: false,
      ready: false,
      map: null,
      canvas: null,
      context: null,
      start: null,
      end: null,
      finish: null,
      currentPos: null,
      solve_speed: 500,
      route: "",
      width: 50,
      height: 50,
      rows: 10,
      cols: 10,
      WSADMap: {
        KeyW: "N",
        KeyS: "S",
        KeyA: "W",
        KeyD: "E"
      },
      arrowMap: {
        ArrowUp: "N",
        ArrowDown: "S",
        ArrowLeft: "W",
        ArrowRight: "E"
      }
    };
  },
  computed: {
    message() {
      if (this.completed) {
        return this.completed.message;
      }
      return null;
    },
    btn_message() {
      if (this.ready) {
        return "Generate new maze";
      }
      return "START";
    }
  },
  methods: {
    resetGame() {
      this.stopTimer();
      this.isFinished = false;
      this.map = null;
      this.route = "";
      this.start = null;
      this.end = null;
      this.finish = null;
      this.currentPos = null;
      this.solve_btn = false;
    },
    newGame() {
      this.completeDialog = false;
      this.resetGame();
      axios.get("/mazebot/random?minSize=10&maxSize=10").then(resp => {
        this.map = resp.data.map;
        this.start = resp.data.startingPosition;
        this.end = resp.data.endingPosition;
        this.finish = resp.data.mazePath;
        this.ready = true;

        this.loadGame();
        this.canvas.focus();
      });
    },
    loadGame() {
      this.canvas = this.$refs.canvas;
      this.context = this.canvas?.getContext("2d");
      this.context.beginPath();

      for (let row = 0; row < this.map.length; row++) {
        for (let col = 0; col < this.map[row].length; col++) {
          if (this.map[row][col] === "A") {
            this.context.fillStyle = "white";
          } else if (this.map[row][col] === "B") {
            this.context.fillStyle = "green";
          } else if (this.map[row][col] === "X") {
            this.context.fillStyle = "black";
          } else {
            this.context.fillStyle = "white";
            this.context.strokeStyle = "black";
          }

          this.context.fillRect(
            this.get_X(col),
            this.get_Y(row),
            this.width,
            this.height
          );

          this.context.strokeRect(
            this.get_X(col),
            this.get_Y(row),
            this.width,
            this.height
          );
        }
      }
      this.context.arc(
        this.get_X(this.start[0]) + this.width / 2,
        this.get_Y(this.start[1]) + this.height / 2,
        20,
        0,
        2 * Math.PI
      );
      this.context.fillStyle = "red";
      this.context.fill();
      this.currentPos = this.start;
    },
    get_X(col) {
      return col * this.width;
    },
    get_Y(row) {
      return row * this.height;
    },
    checkMove(position) {
      if (
        !position.includes(-1) &&
        !position.includes(this.rows) &&
        !position.includes(this.cols)
      ) {
        return !["X", undefined].includes(this.map[position[1]][position[0]]);
      }
    },
    remove() {
      this.context.clearRect(
        this.get_X(this.currentPos[0]) + 5,
        this.get_Y(this.currentPos[1]) + 5,
        this.width - 10,
        this.height - 10
      );
    },
    update(direction) {
      this.context.beginPath();
      let tempPos = null;
      if (direction === "S") {
        tempPos = [this.currentPos[0], this.currentPos[1] + 1];
      } else if (direction === "N") {
        tempPos = [this.currentPos[0], this.currentPos[1] - 1];
      } else if (direction === "W") {
        tempPos = [this.currentPos[0] - 1, this.currentPos[1]];
      } else if (direction === "E") {
        tempPos = [this.currentPos[0] + 1, this.currentPos[1]];
      }

      if (this.checkMove(tempPos)) {
        this.remove();
        this.currentPos = tempPos;

        this.context.arc(
          this.get_X(this.currentPos[0]) + this.width / 2,
          this.get_Y(this.currentPos[1]) + this.height / 2,
          20,
          0,
          2 * Math.PI
        );
        this.context.fillStyle = "red";
        this.context.fill();

        this.route += direction;

        if (
          this.currentPos[0] === this.end[0] &&
          this.currentPos[1] === this.end[1]
        ) {
          this.isFinished = true;
        }
      }
    },
    move(event) {
      if (this.isFinished || this.solve_btn) {
        return;
      }

      let key_pressed = event.code;
      if (key_pressed in this.WSADMap) {
        this.update(this.WSADMap[key_pressed]);
      } else if (key_pressed in this.arrowMap) {
        this.update(this.arrowMap[key_pressed]);
      }

      if (this.isFinished) {
        this.showCompletionDialog();
      }
    },
    showCompletionDialog() {
      axios
        .post(
          this.finish,
          { directions: this.route },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        )
        .then(resp => {
          this.completeDialog = true;
          this.completed = resp.data;
        });
    },
    solve() {
      axios
        .post("http://localhost:5000/getMaze", {
          map: this.map,
          start: this.currentPos,
          end: this.end
        })
        .then(resp => {
          this.solution = resp.data.path;
          this.solve_btn = true;
          let i = 0;
          this.loop(i);
        });
    },
    loop: function(i) {
      this.timer = setTimeout(() => {
        this.update(this.solution[i]);
        if (this.isFinished) {
          this.showCompletionDialog();
        }
        i++;
        if (i < this.solution.length) {
          this.loop(i);
        }
      }, this.solve_speed);
    },
    stopTimer() {
      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = 0;
      }
    }
  }
};
</script>

<style scoped>
.btn {
  margin: 10px;
}
</style>
