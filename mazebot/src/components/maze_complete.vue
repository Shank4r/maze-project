<template>
  <v-dialog
    :value="value"
    :complete="complete"
    @input="$emit('input')"
    max-width="400px"
    persistent
  >
    <v-card>
      <v-card-title class="headline; justify-center"
        >Congratulations!</v-card-title
      >
      <v-card-text>{{ message }}</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click.native="$emit('input')">New Game</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "maze_complete",
  props: ["value", "complete"],
  computed: {
    message() {
      if (this.complete) {
        return this.complete.message;
      }
      return null;
    }
  }
};
</script>

<style scoped></style>
