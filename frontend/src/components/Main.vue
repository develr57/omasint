<script>
import axios from 'axios';
import {mapActions, mapState} from "pinia";


export default {
  name: "Main",
  data() {
    return {
      page_title: 'Главная',
    }
  },
  computed: {
    
  },
  methods: {
    
  },
  created() {
    document.title = this.page_title;
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