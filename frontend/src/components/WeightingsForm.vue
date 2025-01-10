<script>
import axios from "axios";
import {mapState} from "pinia";
import {useApiStore} from "../store/api.js";
import {useUserStore} from "../store/user.js";
import moment from "moment";
import Modal from "./Modal.vue";

export default {
  name: "WeightingsForm",
  components: {Modal},
  data() {
    return {
      weighting: {
        id: null,
        weight: null,
        animal: null,
        animal_name: null,
        breed_name: null,
        animaltype_name: null,
        invent_num: null,
        gender: null,
        user: null,
        username: null,
        created_at: null,
        updated_at: null,
      },
      weight_valid_error: null,
      save_url: null,
      action: null,
      showModalWeightingForbidden: false,
    }
  },
  computed: {
    ...mapState(useApiStore, [
      'API_URL'
    ]),
    ...mapState(useUserStore, [
      'token',
      'user'
    ]),
  },
  created() {
    this.action = this.$route.params.action;
    if (this.$route.params.action === 'edit') {
      this.weighting.id = this.$route.params.id;
      this.getWeighting();
    } else {
      this.weighting.user = this.user.id;
      this.weighting.animal = this.$route.params.id;
      this.getAnimal();
    }
    this.getUrl();
    console.log('router.params: ', this.$route.params);
  },
  methods: {
    async save() {
      let method;
      if (this.action === 'edit') {
        method = 'put';
      } else {
        method = 'post';
      }
      const data = await axios({
        method: method,
        url: this.save_url,
        headers: { Authorization: 'Token ' + this.token },
        data: this.weighting
      }).then((resp) => {
        console.log('save() resp: ', resp);
        if (resp.status === 200 || resp.status === 201) {
          console.log('200 or 201');
          this.$router.go(-1);
        }
      }).catch((error) => {
        console.log('save() error: ', error);
        if (error.code === 'ERR_BAD_REQUEST') {
          if (error.status === 400 && error.response.data.name) {
            this.weight_valid_error = error.response.data.name[0];
          }
          if (error.status === 403 && error.response.data.detail) {
            this.showModalWeightingForbidden = true;
          }
        }
      });
    },
    async getWeighting() {
      const data = await axios.get(`${this.API_URL}/api/v1/weightings/${this.weighting.id}`, {
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('getWeighting resp: ', resp);
        this.weighting = resp.data;
      }).catch(error => {
        console.log('getWeighting error: ', error);
      });
    },
    async getAnimal() {
      const data = await axios.get(`${this.API_URL}/api/v1/animals/${this.weighting.animal}`, {
        headers: { Authorization: 'Token ' + this.token }
      }).then(resp => {
        console.log('getAnimal resp: ', resp);
        // this.weighting = resp.data;
        this.weighting.animal_name = resp.data.name;
        this.weighting.breed_name = resp.data.breed_name;
        this.weighting.animaltype_name = resp.data.animaltype_name;
        this.weighting.invent_num = resp.data.invent_num;
        this.weighting.gender = resp.data.gender;
      }).catch(error => {
        console.log('getAnimal error: ', error);
      });
    },
    getUrl() {
      if (this.weighting.id === null) {
        this.save_url = `${this.API_URL}/api/v1/weightings/`;
      } else {
        this.save_url =  `${this.API_URL}/api/v1/weightings/${this.weighting.id}/`;
      }
    },
    returnGender(gender) {
      if (gender === false) {
        return 'Самка';
      } else if (gender === true) {
        return 'Самец';
      } else {
        return 'Не определён';
      }
    },
    returnDateAndTime(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss');
    },
  },
  watch: {
  }
}
</script>



<template>
  <div class="pt-2">
    <h4 v-if="weighting.id === null">Новое взвешивание</h4>
    <h4 v-if="weighting.id">Редактирование взвешивания</h4>
    <div class="table-responsive mt-4">
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th scope="col">id</th>
            <th scope="col">Инвен. номер</th>
            <th scope="col">Животное</th>
            <th v-if="user.is_superuser && action === 'edit'" scope="col">Пользователь</th>
            <th scope="col" v-if="action === 'edit'">Создан</th>
            <th scope="col" v-if="action === 'edit'">Изменён</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-if="weighting.id !== null">{{ weighting.id }}</td>
            <td v-else>{{ weighting.animal }}</td>
            <td>{{ weighting.invent_num }}</td>
            <td>{{ weighting.animal_name }} ({{ weighting.animaltype_name }}, {{ weighting.breed_name }}, {{ returnGender(weighting.gender) }})</td>
            <td v-if="user.is_superuser && action === 'edit'">{{ weighting.username }}</td>
            <td v-if="action === 'edit'">{{ returnDateAndTime(weighting.created_at) }}</td>
            <td v-if="action === 'edit'">{{ returnDateAndTime(weighting.updated_at) }}</td>
          </tr>
        </tbody>
        <tfoot></tfoot>
      </table>
    </div>
    <div class="pt-2">
      <form @submit.prevent="save">
        <div class="row g-3 align-items-center pb-3">
            <div class="col-sm-12 col-md-3 col-lg-2">
                <label for="inputArrivalAge" class="col-form-label">Вес животного, кг</label>
            </div>
            <div class="col-sm-12 col-md-5 col-lg-4">
                <input v-model.trim="weighting.weight" type="number" step="any" id="inputWeight" class="form-control"
                     aria-labelledby="weightHelpInline">
            </div>
            <div class="col-sm-12 col-md-4 col-lg-6">
                <span id="weightHelpInline" class="form-text" v-if="weight_valid_error === null"></span>
                <span id="weightHelpInline" class="form-text text-danger" v-if="weight_valid_error !== null">
                    {{ weight_valid_error }}
                </span>
            </div>
        </div>

        <div class="pt-2">
          <button type="submit" class="btn btn-success ms-5">Сохранить</button>
        </div>
      </form>
    </div>

  <Teleport to="body">
    <modal :show="showModalWeightingForbidden" @close="showModalWeightingForbidden = false">
      <template #header>
        <h3>Взвешивание запрещено</h3>
      </template>
      <template #body>
        Нельзя взвешивать животное больше одного раза в сутки.
      </template>
      <template #footer>
        <button @click="showModalWeightingForbidden=false; " class="btn btn-primary btn_no">Ok</button>
      </template>
    </modal>
  </Teleport>

  </div>
</template>



<style scoped>

</style>