<script>
import axios from "axios";
import {mapState} from "pinia";
import {useApiStore} from "../store/api.js";
import {useUserStore} from "../store/user.js";

export default {
  name: "BreedsForm",
  data() {
    return {
      breed: {
        id: null,
        name: null,
        animaltype: null,
        animaltype_name: null,
        created_at: null,
        updated_at: null,
      },
      name_valid_error: null,
      animaltype_valid_error: null,
      save_url: null,
      animaltypes: null,
      block_watch: false,
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
      this.breed.id = this.$route.params.id;
      this.getBreed();
    }
    this.getUrl();
  },
  methods: {
    async save() {
      let method;
      if (this.breed.id) {
        method = 'put';
      } else {
        method = 'post';
      }
      const data = await axios({
        method: method,
        url: this.save_url,
        headers: { Authorization: 'Token ' + this.token },
        data: this.breed
      }).then((resp) => {
        console.log('save() resp: ', resp);
        if (resp.status === 200 || resp.status === 201) {
          this.$router.go(-2);
        }
      }).catch((error) => {
        console.log('save() error: ', error);
        if (error.code === 'ERR_BAD_REQUEST') {
          if (error.status === 400 && error.response.data.name) {
            this.name_valid_error = error.response.data.name[0];
          }
          if (error.status === 400 && error.response.data.animaltype) {
            this.animaltype_valid_error = error.response.data.animaltype[0];
          }
        }
      });
    },
    async getBreed() {
      const data = await axios.get(`${this.API_URL}/api/v1/breeds/${this.breed.id}`, {
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('getBreed resp: ', resp);
        this.block_watch = true;
        this.breed = resp.data;
      }).catch(error => {
        console.log('getBreed error: ', error);
      });
    },
    getUrl() {
      if (this.breed.id === null) {
        this.save_url = `${this.API_URL}/api/v1/breeds/`;
      } else {
        this.save_url =  `${this.API_URL}/api/v1/breeds/${this.breed.id}/`;
      }
    },
    async searchAnimalTypes() {
      const data = await axios.get(`${this.API_URL}/api/v1/animaltypes/`, {
        params: {
          limit: 5,
          offset: 0,
          search: this.breed.animaltype_name
        },
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('resp: ', resp);
        if (resp.status === 200 && resp.data.count !== 0) {
          this.animaltypes = resp.data.results;
        }
      }).catch(error => {
        console.log('error: ', error);
      });
    },
    setAnimalType(id, name) {
      this.breed.animaltype = id;
      this.breed.animaltype_name = name;
      this.animaltypes = null;
      this.block_watch = true;
    }
  },
  watch: {
    'breed.animaltype_name': function() {
      if (this.breed.animaltype_name.length > 1 && this.block_watch === false) {
        setTimeout(() => {
          this.searchAnimalTypes();
        }, 500);
      }
      setTimeout(() => {
        this.block_watch = false;
      }, 1000);
      if (this.breed.animaltype_name.length < 2) {
        this.animaltypes = null;
        this.breed.animaltype = null;
      }
    }
  }
}
</script>



<template>
  <div class="pt-2">
    <h4 v-if="breed.id === null">Новая порода животного</h4>
    <h4 v-if="breed.id">Редактирование породы животного</h4>
    <div class="pt-2">
      <form @submit.prevent="save">
        <!--Порода-->
        <div class="row g-3 align-items-center pb-3">
            <div class="col-sm-12 col-md-3 col-lg-2">
                <label for="inputName" class="col-form-label">Порода</label>
            </div>
            <div class="col-sm-12 col-md-5 col-lg-4">
                <input v-model.trim="breed.name" type="text" id="inputName" class="form-control"
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
        <!--Тип животного-->
        <div class="row g-3 align-items-center pb-3">
          <div class="col-sm-12 col-md-3 col-lg-2">
            <label for="inputAnimaltype" class="col-form-label">Тип животного</label>
          </div>
          <div class="col-sm-12 col-md-5 col-lg-4">
            <input v-model.trim="breed.animaltype_name" type="text" id="inputAnimaltype" class="form-control"
               aria-labelledby="animaltypeHelpInline" placeholder="Начните ввод и выберите вариант">
            <input v-model="breed.animaltype" type="number" id="inputAnimaltype" class="form-control" hidden>
            <div class="searched-box" v-if="animaltypes !== null">
              <ul><li>Выберите нужный вариант</li>
                <li v-for="animaltype in animaltypes" :key="animaltype.id"><a href="#"
                   @click="setAnimalType(animaltype.id, animaltype.name)">{{ animaltype.name }}</a></li>
              </ul>
            </div>
          </div>
          <div class="col-sm-12 col-md-4 col-lg-6">
            <span id="animaltypeHelpInline" class="form-text" v-if="animaltype_valid_error === null">
            </span>
            <span id="animaltypeHelpInline" class="form-text text-danger" v-if="animaltype_valid_error !== null">
                {{ animaltype_valid_error }}
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