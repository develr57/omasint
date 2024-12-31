<script>
import { mapActions, mapState } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../store/user';
import { useApiStore } from '../store/api';


export default {
  name: "Login",
  data() {
    return {
      username: '',
      password: '',
      auth_error: false,
      auth_error_text: 'Неверное имя пользователя или пароль'
    }
  },
  computed: {
    ...mapState(useUserStore, [
      'userIsAuth'
    ]),
    ...mapState(useApiStore, [
        'API_URL',
    ]),
  },
  watch: {
    userIsAuth() {
      this.$router.push('/');
    },
  },
  methods: {
    ...mapActions(useUserStore, [
      'storeLoggedInUser',
      'storeAuthToken'
    ]),
    async login() {
      const data = axios.post(`${this.API_URL}/auth/token/login/`, {
          username: this.username,
          password: this.password
        },
      ).then(resp => {
        this.token = resp.data.auth_token;
        this.storeAuthToken(this.token);
        this.userInfo();
      }).catch(error => {
        console.log(error);
        if (error.status == 400) {
          this.auth_error = true;
        } else {
          alert('Не удалось получить данные!');
        }
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
        this.storeLoggedInUser(resp.data);
      }).catch(error => {
        alert('Не удалось получить данные!');
      });
    }
  }
}
</script>

<template>
  <div class="">
    <div class="col-md-4 offset-4 border border-1 p-3 position-absolute login-form">
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Имя пользователя</label>
          <input v-model.trim="username" type="username" class="form-control" id="username" aria-describedby="username">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Пароль</label>
          <input v-model.trim="password" type="password" class="form-control" id="password" autocomplete="on">
        </div>
        <div class="form-text text-danger pb-3" v-if="auth_error">{{ auth_error_text }}</div>
        <button type="submit" class="btn btn-primary">Отправить</button>
        <div class="reg-link pt-1">
          <RouterLink to="/register">Регистрация</RouterLink>
        </div>
      </form>
    </div>  
  </div>
</template>

<style scoped>
.login-form {
  left: 0;
  top:30%;
}
.reg-link {
  float: right;
}
</style>