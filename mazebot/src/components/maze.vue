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
            :height="heigth * rows"
            style="border: 1px solid black; display: block; margin-right: auto; margin-left: auto;"
            @keyup="move"
            tabindex="0"
          >
          </canvas>
          <v-btn @click="newGame" v-if="!ready">New Game</v-btn>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";
import testmap from "raw-loader!../assets/testmap.txt";

export default {
  name: "maze",
  data() {
    return {
      isFinsihed: false,
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
      route: "",
      width: 50,
      heigth: 50,
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
    }
  },
  created() {
    axios.post("http://localhost:5000/getMaze", { maze: JSON.parse(testmap) });
  },
  methods: {
    resetGame() {
      this.isFinsihed = false;
      this.map = null;
      this.route = "";
      this.start = null;
      this.end = null;
      this.finish = null;
      this.currentPos = null;
    },
    newGame() {
      this.completeDialog = false;
      this.resetGame();
      // axios.get("/mazebot/random?minSize=10&maxSize=10").then(resp => {
      let resp_data = JSON.parse(testmap);
      this.map = resp_data.map;
      this.start = resp_data.startingPosition;
      this.end = resp_data.endingPosition;
      this.finish = resp_data.mazePath;
      this.ready = true;

      this.loadGame();
      this.canvas.focus();
      // axios.post("http://localhost:5000/getMaze", { maze: resp.data });
      //  });
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
            this.heigth
          );

          this.context.strokeRect(
            this.get_X(col),
            this.get_Y(row),
            this.width,
            this.heigth
          );
        }
      }
      this.context.arc(
        this.get_X(this.start[0]) + this.width / 2,
        this.get_Y(this.start[1]) + this.heigth / 2,
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
      return row * this.heigth;
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
        this.heigth - 10
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
          this.get_Y(this.currentPos[1]) + this.heigth / 2,
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
          this.isFinsihed = true;
        }
      }
    },
    move(event) {
      if (this.isFinsihed) {
        return;
      }

      let key_pressed = event.code;
      if (key_pressed in this.WSADMap) {
        this.update(this.WSADMap[key_pressed]);
      } else if (key_pressed in this.arrowMap) {
        this.update(this.arrowMap[key_pressed]);
      }

      if (this.isFinsihed) {
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
      }
    }
  }
};
</script>

<style scoped></style>
