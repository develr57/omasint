<script>
import { mapActions, mapState } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../store/user';
import { useApiStore } from '../store/api';
import Modal from "./Modal.vue";
import { useWeightingsStore } from "../store/weightings.js";
import moment from 'moment';
import {useRoutingStore} from "../store/routing.js";


export default {
  name: "Weightings",
  components: {
    Modal,
  },
  data() {
    return {
      weightings: [],
      pagin_list: [],
      start: null,
      end: null,
      showModal: false,
      confirm_delete: false,
      deleted_id: null,
      deleted_name: null,
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
    ...mapState(useWeightingsStore, [
        'getPageSize',
        'getTotalItems',
        'getCurrPage',
        'getOffset',
        'getTotalPages',
    ]),
  },
  methods: {
    ...mapActions(useWeightingsStore, [
      'setPageSize',
      'setTotalItems',
      'setCurrPage',
      'setOffset',
      'setTotalPages'
    ]),
    ...mapActions(useRoutingStore, [
        'setCurrRouteName'
    ]),
    async getWeightings() {
      const data = await axios.get(`${this.API_URL}/api/v1/weightings/`, {
        params: {
          limit: this.getPageSize,
          offset: this.getOffset,
        },
        headers: {
          Authorization: 'Token ' + this.token
        }
      }).then(resp => {
        console.log('getWeightings resp: ', resp);
        this.weightings = resp.data.results;
        this.setTotalItems(resp.data.count);
        this.setTotalPages(Math.ceil(this.getTotalItems / this.getPageSize));
        this.setPagRange();
        this.pagin_list = this.getPagBtnArray(this.start, this.end);
      }).catch(error => {
        console.log('error: ', error);
      });
    },
    getPagBtnArray(start, end) {
      let arr = [];
      for (let i = start; i <= end; i++) {
        arr.push(i);
      }
      return arr;
    },
    setPagRange() {
      if (this.getCurrPage <= 5) {
        this.start = 1;
      } else {
        this.start = this.getCurrPage - 4;
      }
      if (this.getTotalPages <= 10) {
        this.end = this.getTotalPages;
      }
      if ((this.getCurrPage + 5) === this.getTotalPages) {
        this.end = this.getTotalPages;
      }
      if ((this.getCurrPage + 5) < this.getTotalPages) {
        this.end = this.getCurrPage + 5;
      }
    },
    pagBtnIsActive(n) {
      return Number(this.getCurrPage) === Number(n);
    },
    async deleteWeighting(id) {
      if (this.confirm_delete === true) {
        const data = await axios.delete(`${this.API_URL}/api/v1/weightings/${id}/`,{
          params: {},
          headers: {
            Authorization: 'Token ' + this.token
          }
        }).then(resp => {
          console.log('delete resp: ', resp);
          if (resp.status === 204) {
            this.getWeightings();
          }
        }).catch(error => {
          console.log('delete error: ', error);
        });
      }
      this.resetDeleted();
    },
    confirmationDelete(id) {
      this.confirm_delete = false;
      this.deleted_id = id;
      // this.deleted_name = name;
      this.showModal = true;
    },
    resetDeleted() {
      this.confirm_delete = false;
      this.deleted_id = null;
      this.deleted_name = null;
      this.showModal = false;
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
  created() {
    this.setCurrPage(this.$route.params.page);
    this.setOffset((this.getCurrPage - 1) * this.getPageSize);
    this.getWeightings();
    this.setCurrRouteName(this.$route.name);
    document.title = 'Взвешивания';
  },
  watch: {
    '$route.params.page': function () {
      this.setCurrPage(this.$route.params.page);
      this.setOffset((this.getCurrPage - 1) * this.getPageSize);
      this.getWeightings();
    }
  }
}
</script>

<template>
  <div>
    <h3 class="mt-4">Мои взвешивания</h3>
    <div class="table-responsive mt-4">
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th scope="col">id</th>
            <th scope="col">Инвен. номер</th>
            <th scope="col">Животное</th>
            <th scope="col">Вес</th>
            <th v-if="user.is_superuser" scope="col">Пользователь</th>
            <th scope="col">Создан</th>
            <th scope="col">Изменён</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="weighting in weightings" :key="weighting.id">
            <td>{{ weighting.id }}</td>
            <td>{{ weighting.invent_num }}</td>
            <td>{{ weighting.animal_name }} ({{ weighting.animaltype_name }}, {{ weighting.breed_name }}, {{ returnGender(weighting.gender) }})</td>
            <td><RouterLink :to="`/weightings/edit/${weighting.id}`">{{ weighting.weight }}</RouterLink></td>
            <td v-if="user.is_superuser">{{ weighting.username }}</td>
            <td>{{ returnDateAndTime(weighting.created_at) }}</td>
            <td>{{ returnDateAndTime(weighting.updated_at) }}</td>
            <td><a @click="confirmationDelete(weighting.id)" href="#" class="btn">❌</a></td>
          </tr>
        </tbody>
        <tfoot></tfoot>
      </table>
    </div>

<!--    <div>-->
<!--      <RouterLink to="/weightings/add" class="btn btn-success">Добавить</RouterLink>-->
<!--    </div>-->
    <div class="mt-2">
      <RouterLink v-for="n in pagin_list" class="btn btn-primary mx-1" :class="{ activePagBtn: pagBtnIsActive(n) }"
        :to="`/weightings/page/${n}`">{{ n }}</RouterLink>
    </div>

<!--    <button id="show-modal" @click="showModal = true">Показать модальное окно</button>-->
    <Teleport to="body">
      <modal :show="showModal" @close="showModal = false">
        <template #header>
          <h3>Вы уверены?</h3>
        </template>
        <template #body>
          Действительно хотите удалить взвешивание с идентификатором {{ deleted_id }}?
        </template>
        <template #footer>
          <button @click="showModal=false; confirm_delete=true; deleteWeighting(this.deleted_id)"
                  class="btn btn-danger btn_yes">Да</button>
          <button @click="showModal=false; resetDeleted()" class="btn btn-primary btn_no">Нет</button>
        </template>
      </modal>
    </Teleport>

  </div>
</template>

<style scoped>
  .activePagBtn {
    background-color: orange !important;
  }
  .modal-header h3 {
    margin-top: 0;
    color: #42b983;
  }
  .btn_yes {
    float: left;
  }
  .btn_no {
    float: right;
  }
</style>