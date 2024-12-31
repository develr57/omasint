<script>
import axios from 'axios';
import { useRoutingStore } from "../store/routing.js";
import {mapActions, mapState} from "pinia";


export default {
  name: "Main",
  data() {
    return {
    }
  },
  computed: {
    ...mapState(useRoutingStore, [
        'curr_route_name',
    ])
  },
  methods: {
    ...mapActions(useRoutingStore, [
        'setCurrRouteName'
    ])
  },
  created() {
    this.setCurrRouteName(this.$route.name);
    document.title = 'Главная';
  }
}
</script>

<template>
  <div>
    <h1>Main</h1>
  </div>
</template>

<style scoped>

</style>