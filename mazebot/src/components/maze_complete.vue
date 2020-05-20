<template>
  <v-dialog :value="value" :complete="complete" @input="$emit('input')" max-width="600px" persistent>
    <v-card>
      <v-card-title class="headline">Congratulations!</v-card-title>
        <v-card-text>{{ value }}</v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "maze_complete",
  props: ["value", "complete"]
};
</script>

<style scoped></style>
