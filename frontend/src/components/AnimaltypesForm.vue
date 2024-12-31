<script>
import axios from "axios";
import {mapState} from "pinia";
import {useApiStore} from "../store/api.js";
import {useUserStore} from "../store/user.js";

export default {
  name: "AnimaltypesForm",
  data() {
    return {
      animaltype: {
        id: null,
        name: null,
        created_at: null,
        updated_at: null,
      },
      name_valid_error: null,
      save_url: null,
    }
  },
  computed: {
    ...mapState(useApiStore, [
      'API_URL'
    ]),
    ...mapState(useUserStore, [
      'token',
    ]),
  },
  created() {
    if (this.$route.params.id !== undefined) {
      this.animaltype.id = this.$route.params.id;
      this.getAnimaltype();
    }
    this.getUrl();
  },
  methods: {
    async save() {
      let method;
      if (this.animaltype.id) {
        method = 'put';
        // console.log('method: ', method);
      } else {
        method = 'post';
        // console.log('method: ', method);
      }
      const data = await axios({
        method: method,
        url: this.save_url,
        headers: { Authorization: 'Token ' + this.token },
        data: this.animaltype
      }).then((resp) => {
        // console.log('save() resp: ', resp);
        if (resp.status === 200 || resp.status === 201) {
          // this.$router.push('/animaltypes/page/1');
          this.$router.back();
        }
      }).catch((error) => {
        // console.log('error: ', error);
        if (error.code === 'ERR_BAD_REQUEST') {
          if (error.status === 400 && error.response.data.name) {
            this.name_valid_error = error.response.data.name[0];
          }
        }
      });
    },
    async getAnimaltype() {
      const data = await axios.get(`${this.API_URL}/api/v1/animaltypes/${this.animaltype.id}`, {
        headers: {
          Authorization: 'Token ' + this.token
        }
      }).then(resp => {
        console.log('getAnimaltype resp: ', resp);
        this.animaltype = resp.data;
      }).catch(error => {
        console.log('getAnimaltype error: ', error);
      });
    },
    getUrl() {
      if (this.animaltype.id === null) {
        this.save_url = `${this.API_URL}/api/v1/animaltypes/`;
      } else {
        this.save_url =  `${this.API_URL}/api/v1/animaltypes/${this.animaltype.id}/`;
      }
    }
  }
}
</script>



<template>
  <div class="pt-2">
    <h4 v-if="animaltype.id === null">Новый тип животного</h4>
    <h4 v-if="animaltype.id">Редактирование типа животного</h4>
    <div class="pt-2">
      <form @submit.prevent="save">
        <div class="row g-3 align-items-center pb-3">
            <div class="col-sm-12 col-md-3 col-lg-2">
                <label for="inputName" class="col-form-label">Наименование</label>
            </div>
            <div class="col-sm-12 col-md-5 col-lg-4">
                <input v-model.trim="animaltype.name" type="text" id="inputName" class="form-control"
                     aria-labelledby="nameHelpInline">
            </div>
            <div class="col-sm-12 col-md-4 col-lg-6">
                <span id="nameHelpInline" class="form-text" v-if="name_valid_error === null">
                  Должно быть уникальным
                </span>
                <span id="nameHelpInline" class="form-text text-danger" v-if="name_valid_error !== null">
                    {{ name_valid_error }}
                </span>
            </div>
        </div>
        <div class="pt-2">
          <button type="submit" class="btn btn-success ms-5">Сохранить</button>
        </div>
      </form>
    </div>
  </div>
</template>



<style scoped>

</style>