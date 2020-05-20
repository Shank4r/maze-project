import Vue from "vue";
import VueRouter from "vue-router";
import Maze from "../components/maze.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Maze",
    component: Maze
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
