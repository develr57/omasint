<script>
import axios from "axios";
import {mapState} from "pinia";
import {useApiStore} from "../store/api.js";
import {useUserStore} from "../store/user.js";

export default {
  name: "AnimalsForm",
  data() {
    return {
      animal: {
        id: null,
        name: null,
        breed: null,
        breed_name: null,
        animaltype: null,
        animaltype_name: null,
        invent_num: null,
        arrival_date: null,
        arrival_age: null,
        parent: null,
        parent_name: null,
        created_at: null,
        updated_at: null,
      },
      name_valid_error: null,
      invent_num_valid_error: null,
      breed_valid_error: null,
      gender_valid_error: null,
      arrival_date_valid_error: null,
      arrival_age_valid_error: null,
      parent_valid_error: null,
      save_url: null,
      breeds: null,
      block_watch: false,
      animals: null,
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
      this.animal.id = this.$route.params.id;
      this.getAnimal();
    }
    this.getUrl();
  },
  methods: {
    async save() {
      let method;
      if (this.animal.id) {
        method = 'put';
      } else {
        method = 'post';
      }
      const data = await axios({
        method: method,
        url: this.save_url,
        headers: { Authorization: 'Token ' + this.token },
        data: this.animal
      }).then((resp) => {
        console.log('save() resp: ', resp);
        if (resp.status === 200 || resp.status === 201) {
          console.log('200 or 201');
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
          if (error.status === 400 && error.response.data.breed) {
            this.breed_valid_error = error.response.data.breed[0];
          }
          if (error.status === 400 && error.response.data.invent_num) {
            this.invent_num_valid_error = error.response.data.invent_num[0];
          }
          if (error.status === 400 && error.response.data.arrival_date) {
            this.arrival_date_valid_error = error.response.data.arrival_date[0];
          }
          if (error.status === 400 && error.response.data.arrival_age) {
            this.arrival_age_valid_error = error.response.data.arrival_age[0];
          }
        }
      });
    },
    async getAnimal() {
      const data = await axios.get(`${this.API_URL}/api/v1/animals/${this.animal.id}`, {
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('getAnimal resp: ', resp);
        this.block_watch = true;
        this.animal = resp.data;
      }).catch(error => {
        console.log('getAnimal error: ', error);
      });
    },
    getUrl() {
      if (this.animal.id === null) {
        this.save_url = `${this.API_URL}/api/v1/animals/`;
      } else {
        this.save_url =  `${this.API_URL}/api/v1/animals/${this.animal.id}/`;
      }
    },
    async searchBreeds() {
      const data = await axios.get(`${this.API_URL}/api/v1/breeds/`, {
        params: {
          limit: 5,
          offset: 0,
          search: this.animal.breed_name
        },
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('searchBreeds resp: ', resp);
        if (resp.status === 200 && resp.data.count !== 0) {
          this.breeds = resp.data.results;
        }
      }).catch(error => {
        console.log('searchBreeds error: ', error);
      });
    },
    setBreed(id, name) {
      this.animal.breed = id;
      this.animal.breed_name = name;
      this.breeds = null;
      this.block_watch = true;
    },
    async searchAnimals() {
      const data = await axios.get(`${this.API_URL}/api/v1/animals/`, {
        params: {
          limit: 5,
          offset: 0,
          search: this.animal.parent_name
        },
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('searchAnimals resp: ', resp);
        if (resp.status === 200 && resp.data.count !== 0) {
          this.animals = resp.data.results;
        }
      }).catch(error => {
        console.log('searchBreeds error: ', error);
      });
    },
    setParent(id, name) {
      this.animal.parent = id;
      this.animal.parent_name = name;
      this.animals = null;
      this.block_watch = true;
    }
  },
  watch: {
    'animal.breed_name': function() {
      if (this.animal.breed_name.length > 1 && this.block_watch === false) {
        setTimeout(() => {
          this.searchBreeds();
        }, 500);
      }
      setTimeout(() => {
        this.block_watch = false;
      }, 1000);
      if (this.animal.breed_name.length < 2) {
        this.breeds = null;
        this.animal.breed = null;
      }
    },
    'animal.parent_name': function() {
      if (this.animal.parent_name.length > 1 && this.block_watch === false) {
        setTimeout(() => {
          this.searchAnimals();
        }, 500);
      }
      setTimeout(() => {
        this.block_watch = false;
      }, 1000);
      if (this.animal.parent_name.length < 2) {
        this.animals = null;
        this.animal.parent = null;
      }
    }
  }
}
</script>



<template>
  <div class="pt-2">
    <h4 v-if="animal.id === null">Новое животное</h4>
    <h4 v-if="animal.id">Редактирование животного</h4>
    <div class="pt-2">
      <form @submit.prevent="save">
        <!--Порода-->
        <div class="row g-3 align-items-center pb-3">
          <div class="col-sm-12 col-md-3 col-lg-2">
            <label for="inputName" class="col-form-label">Кличка</label>
          </div>
          <div class="col-sm-12 col-md-5 col-lg-4">
            <input v-model.trim="animal.name" type="text" id="inputName" class="form-control"
                 aria-labelledby="nameHelpInline">
          </div>
          <div class="col-sm-12 col-md-4 col-lg-6">
            <span id="nameHelpInline" class="form-text" v-if="name_valid_error === null"></span>
            <span id="nameHelpInline" class="form-text text-danger" v-if="name_valid_error !== null">
                {{ name_valid_error }}
            </span>
          </div>
        </div>
        <!--Порода-->
        <div class="row g-3 align-items-center pb-3">
          <div class="col-sm-12 col-md-3 col-lg-2">
            <label for="inputAnimaltype" class="col-form-label">Порода</label>
          </div>
          <div class="col-sm-12 col-md-5 col-lg-4">
            <input v-model.trim="animal.breed_name" type="text" id="inputAnimaltype" class="form-control"
               aria-labelledby="animaltypeHelpInline" placeholder="Начните ввод и выберите вариант">
            <input v-model="animal.breed" type="number" id="inputAnimaltype" class="form-control" hidden>
            <div class="searched-box" v-if="breeds !== null">
              <ul><li>Выберите нужный вариант</li>
                <li v-for="breed in breeds" :key="breed.id"><a href="#" @click="setBreed(breed.id, breed.name)">{{ breed.name }} ({{ breed.animaltype_name }})</a></li>
              </ul>
            </div>
          </div>
          <div class="col-sm-12 col-md-4 col-lg-6">
            <span id="animaltypeHelpInline" class="form-text" v-if="breed_valid_error === null"></span>
            <span id="animaltypeHelpInline" class="form-text text-danger" v-if="breed_valid_error !== null">
                {{ breed_valid_error }}
            </span>
          </div>
        </div>
        <!--Инвентарный номер-->
        <div class="row g-3 align-items-center pb-3">
          <div class="col-sm-12 col-md-3 col-lg-2">
            <label for="inputInventNum" class="col-form-label">Инвентарный номер</label>
          </div>
          <div class="col-sm-12 col-md-5 col-lg-4">
            <input v-model.trim="animal.invent_num" type="text" id="inputInventNum" class="form-control"
                 aria-labelledby="inventNumHelpInline">
          </div>
          <div class="col-sm-12 col-md-4 col-lg-6">
            <span id="inventNumHelpInline" class="form-text" v-if="invent_num_valid_error === null"></span>
            <span id="inventNumHelpInline" class="form-text text-danger" v-if="invent_num_valid_error !== null">
                {{ invent_num_valid_error }}
            </span>
          </div>
        </div>
        <!--Пол-->
        <div class="row g-3 align-items-center pb-3">
          <div class="col-sm-12 col-md-3 col-lg-2">
              <label for="inputGender" class="col-form-label">Пол</label>
          </div>
          <div class="col-sm-12 col-md-5 col-lg-4">
            <select v-model.trim="animal.gender" id="inputGender" class="form-select"
                 aria-labelledby="genderHelpInline">
              <option :value="null" selected>Не определён</option>
              <option :value="true">Самец</option>
              <option :value="false">Самка</option>
            </select>
          </div>
          <div class="col-sm-12 col-md-4 col-lg-6">
            <span id="genderHelpInline" class="form-text" v-if="gender_valid_error === null">Выберите пол</span>
            <span id="genderHelpInline" class="form-text text-danger" v-if="gender_valid_error !== null">
                {{ gender_valid_error }}
            </span>
          </div>
        </div>
        <!--Дата поступления-->
        <div class="row g-3 align-items-center pb-3">
            <div class="col-sm-12 col-md-3 col-lg-2">
                <label for="inputArrivalDate" class="col-form-label">Дата поступления</label>
            </div>
            <div class="col-sm-12 col-md-5 col-lg-4">
                <input v-model.trim="animal.arrival_date" type="date" id="inputArrivalDate" class="form-control"
                     aria-labelledby="arrivalDateHelpInline">
            </div>
            <div class="col-sm-12 col-md-4 col-lg-6">
                <span id="arrivalDateHelpInline" class="form-text" v-if="arrival_date_valid_error === null"></span>
                <span id="arrivalDateHelpInline" class="form-text text-danger" v-if="arrival_date_valid_error !== null">
                    {{ arrival_date_valid_error }}
                </span>
            </div>
        </div>
        <!--Возраст поступления-->
        <div class="row g-3 align-items-center pb-3">
            <div class="col-sm-12 col-md-3 col-lg-2">
                <label for="inputArrivalAge" class="col-form-label">Возраст поступления в месяцах</label>
            </div>
            <div class="col-sm-12 col-md-5 col-lg-4">
                <input v-model.trim="animal.arrival_age" type="number" id="inputArrivalAge" class="form-control"
                     aria-labelledby="arrivalAgeHelpInline">
            </div>
            <div class="col-sm-12 col-md-4 col-lg-6">
                <span id="arrivalAgeHelpInline" class="form-text" v-if="arrival_age_valid_error === null"></span>
                <span id="arrivalAgeHelpInline" class="form-text text-danger" v-if="arrival_age_valid_error !== null">
                    {{ arrival_age_valid_error }}
                </span>
            </div>
        </div>
        <!--Родитель-->
        <div class="row g-3 align-items-center pb-3">
          <div class="col-sm-12 col-md-3 col-lg-2">
            <label for="inputParent" class="col-form-label">Родитель</label>
          </div>
          <div class="col-sm-12 col-md-5 col-lg-4">
            <input v-model.trim="animal.parent_name" type="text" id="inputParent" class="form-control"
               aria-labelledby="parentHelpInline" placeholder="Начните ввод и выберите вариант">
            <input v-model="animal.parent" type="number" id="inputParent" class="form-control" hidden>
            <div class="searched-box" v-if="animals !== null">
              <ul><li>Выберите нужный вариант</li>
                <li v-for="animal in animals" :key="animal.id"><a href="#" @click="setParent(animal.id, animal.name)"
                >{{ animal.name }} ({{ animal.breed_name }})</a></li>
              </ul>
            </div>
          </div>
          <div class="col-sm-12 col-md-4 col-lg-6">
            <span id="parentHelpInline" class="form-text" v-if="parent_valid_error === null"></span>
            <span id="parentHelpInline" class="form-text text-danger" v-if="parent_valid_error !== null">
                {{ parent_valid_error }}
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