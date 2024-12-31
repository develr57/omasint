<script>
import axios from 'axios';
import { useUserStore } from './store/user';
import { useApiStore } from './store/api';
import { useRoutingStore } from "./store/routing.js";
import { mapActions, mapState } from 'pinia';

export default {
  name: "App",
  data() {
    return {
      open_error_modal: false,
      error_modal_text: null,
      mainActive: false,
      animaltypesActive: false,
      breedsActive: false,
      animalsActive: false,
      weightingsActive: false
    }
  },
  computed: {
    ...mapState(useUserStore, [
      'userIsAuth',
      'token',
      'user',
    ]),
    ...mapState(useApiStore, [
      'API_URL'
    ]),
    ...mapState(useRoutingStore, [
        'curr_route_name',
        'getCurrRouteName'
    ])
  },
  methods: {
    ...mapActions(useUserStore, [
        'logoutUser',
        'storeLoggedInUser'
    ]),
    ...mapActions(useRoutingStore, [
        'setCurrRouteName'
    ]),
    logout() {
      axios.post(`${this.API_URL}/auth/token/logout`, {}, {
        headers: { 'Authorization': 'Token ' + this.token }
      }).then(resp => {
        console.log(resp.data);
        this.logoutUser();
      });
    },
    async userInfo() {
      const data = await axios({
        method: 'get',
        url: `${this.API_URL}/api/v1/auth/users/me`,
        headers: {
          'Authorization': 'Token ' + this.token
        },
      }).then(resp => {
        // console.log('user: ', resp.data);
        this.storeLoggedInUser(resp.data);
      }).catch(error => {
        alert('Не удалось получить данные!');
      });
    }
  },
  created() {
    if (!this.user && this.userIsAuth) {
      this.userInfo();
    }
  },
  watch: {
    userIsAuth: function() {
      if (!this.userIsAuth) {
        this.$router.push('/login');
      }
    },
    curr_route_name: function () {
      this.mainActive = false;
      this.animaltypesActive = false;
      this.breedsActive = false;
      this.animalsActive = false;
      this.weightingsActive = false;
      if (this.curr_route_name === 'Main') {
        this.mainActive = true;
      }
      if (this.curr_route_name === 'Animaltypes') {
        this.animaltypesActive = true;
      }
      if (this.curr_route_name === 'Breeds') {
        this.breedsActive = true;
      }
      if (this.curr_route_name === 'Animals') {
        this.animalsActive = true;
      }
      if (this.curr_route_name === 'Weightings') {
        this.weightingsActive = true;
      }
    }
  }
}
</script>

<template>
  <div class="container-fluid app-container">
    <header>
      <div class="row">
        <div class="col-md-8 border border-1">
          <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
              <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                  <RouterLink to="/" class="nav-link" :class="{active: mainActive}" href="#">Главная</RouterLink>
                  <RouterLink to="/animaltypes/page/1" class="nav-link" :class="{active: animaltypesActive}" href="#"
                    >Типы животных</RouterLink>
                  <RouterLink to="/breeds/page/1"  class="nav-link" :class="{active: breedsActive}"  href="#"
                    >Породы</RouterLink>
                  <RouterLink to="/animals/page/1"  class="nav-link" :class="{active: animalsActive}" href="#"
                    >Животные</RouterLink>
                  <RouterLink to="/weightings/page/1"  class="nav-link" :class="{active: weightingsActive}" href="#"
                    >Взвешивания</RouterLink>
                </div>
              </div>
            </div>
          </nav>
        </div>
        <div class="col-md-4 border border-1 d-inline-flex flex-nowrap align-items-center justify-content-end">
          <div class="p-1" v-if="user">{{user.username}}</div>
          <div class="p-1"><a v-if="userIsAuth" href="#" @click="logout">Выход</a></div>
        </div>
      </div>
    </header>
    <RouterView />
  </div>
</template>

<style scoped>
  .app-container {
    max-width: 1200px;
  }
  .error_modal {
    border: 1px solid;
    border-radius: 0.5em;
    max-width: fit-content;
    position: fixed;
    z-index: 999;
    left: 40%;
    top: 40%;
    background-color: white;
  }
  .active {
    background-color: white;
    border-radius: 0.5em;
    font-weight: bolder;
  }
</style>