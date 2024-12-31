<script>
import { mapActions, mapState } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../store/user';
import { useApiStore } from '../store/api';


export default {
  name: "Activation",
  data() {
    return {
      uid: this.$route.params.uid,
      token: this.$route.params.token,
      error_message: null,
      request_complete: false,
      success: null,
    }
  },
  computed: {
    ...mapState(useApiStore, [
        'API_URL',
    ]),
  },
  created() {
    this.activate();
  },
  methods: {
    async activate() {
      const data = await axios.post(`${this.API_URL}/api/v1/auth/users/activation/`, {
        uid: this.uid,
        token: this.token,
      }).then(resp => {
        if (resp.status === 204) {
          this.success = true;
        }
        this.request_complete = true;
      }).catch(error => {
        console.log('error: ', error);
        this.request_complete = true;
        if (error.code === 'ERR_NETWORK') {
          this.error_message = 'Ошибка сети!';
        } else if (error.code === 'ERR_BAD_REQUEST') {
          if (error.status === 400) {
            if (error.response.data.uid) {
              this.error_message = error.response.data.uid[0];
            } else if (error.response.data.token) {
              this.error_message = error.response.data.token[0];
            }
          } else if (error.status === 403) {
            this.error_message = error.response.data.detail;
          } else if (error.status === 404) {
            this.error_message = 'Ошибка! Сервер не найден.';
          }
        } else {
          this.error_message = error.message;
        }
      });
    }
  }
}
</script>

<template>
  <div class="pt-3">
    <h3>Активация аккаунта...</h3>
    <div class="spinner-border text-secondary" role="status" v-if="request_complete === false"></div>
    <div v-if="error_message">
      <p class="text-danger">{{ error_message }}</p>
    </div>
    <div v-if="success === true" class="text-success">
      <p>Аккаунт активирован. Теперь можете <RouterLink to="/login">войти</RouterLink>.</p>
    </div>
  </div>
</template>

<style scoped>

</style>