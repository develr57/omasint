<script>
import { mapActions, mapState } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../store/user';
import { useApiStore } from '../store/api';
import Modal from "./Modal.vue";
import { useAnimalsStore } from "../store/animals.js";
import moment from 'moment';


export default {
  name: "Animals",
  components: {
    Modal,
  },
  data() {
    return {
      page_title: 'Животные',
      animals: [],
      pagin_list: [],
      start: null,
      end: null,
      showModal: false,
      confirm_delete: false,
      deleted_id: null,
      deleted_name: null,
      showModalDelImpossible: false,
      parent_delete_error: null,
    }
  },
  computed: {
    ...mapState(useApiStore, [
      'API_URL'
    ]),
    ...mapState(useUserStore, [
      'token',
    ]),
    ...mapState(useAnimalsStore, [
        'getPageSize',
        'getTotalItems',
        'getCurrPage',
        'getOffset',
        'getTotalPages',
    ]),
  },
  methods: {
    ...mapActions(useAnimalsStore, [
      'setPageSize',
      'setTotalItems',
      'setCurrPage',
      'setOffset',
      'setTotalPages'
    ]),
    async getAnimals() {
      const data = await axios.get(`${this.API_URL}/api/v1/animals/`, {
        params: {
          limit: this.getPageSize,
          offset: this.getOffset,
        },
        headers: {
          Authorization: 'Token ' + this.token
        }
      }).then(resp => {
        console.log('getAnimals resp: ', resp);
        this.animals = resp.data.results;
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
    async deleteAnimal(id) {
      if (this.confirm_delete === true) {
        const data = await axios.delete(`${this.API_URL}/api/v1/animals/${id}/`,{
          params: {},
          headers: {
            Authorization: 'Token ' + this.token
          }
        }).then(resp => {
          console.log('delete resp: ', resp);
          if (resp.status === 204) {
            this.getAnimals();
          }
        }).catch(error => {
          console.log('delete error: ', error);
          if (error.status === 403 && error.response.data.detail) {
            this.parent_delete_error = error.response.data.detail;
            this.showModalDelImpossible = true;
          }
        });
      }
      this.resetDeleted();
    },
    confirmationDelete(id, name) {
      this.confirm_delete = false;
      this.deleted_id = id;
      this.deleted_name = name;
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
    this.getAnimals();
    document.title = this.page_title;
  },
  watch: {
    '$route.params.page': function () {
      this.setCurrPage(this.$route.params.page);
      this.setOffset((this.getCurrPage - 1) * this.getPageSize);
      this.getAnimals();
    }
  }
}
</script>

<template>
  <div>
    <h3 class="mt-4">Животные</h3>
    <div class="table-responsive mt-4">
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th scope="col">id</th>
            <th scope="col">Кличка</th>
            <th scope="col">Тип (порода)</th>
            <th scope="col">Инв. номер</th>
            <th scope="col">Пол</th>
            <th scope="col">Дата поступления</th>
            <th scope="col">Возраст поступления</th>
            <th scope="col">Родитель</th>
            <th scope="col">Создан</th>
            <th scope="col">Изменён</th>
            <th scope="col"></th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="animal in animals" :key="animal.id">
            <td>{{ animal.id }}</td>
            <td><RouterLink :to="`/animals/edit/${animal.id}`">{{ animal.name }}</RouterLink></td>
            <td>{{ animal.animaltype_name }}({{ animal.breed_name }})</td>
            <td>{{ animal.invent_num }}</td>
            <td>{{ returnGender(animal.gender) }}</td>
            <td>{{ animal.arrival_date }}</td>
            <td>{{ animal.arrival_age }}</td>
            <td>{{ animal.parent_name || 'Не определён' }}</td>
            <td>{{ returnDateAndTime(animal.created_at) }}</td>
            <td>{{ returnDateAndTime(animal.updated_at) }}</td>
            <td><RouterLink :to="`/weightings/add/${animal.id}`" class="btn btn-primary">Взвесить</RouterLink></td>
            <td><a @click="confirmationDelete(animal.id, animal.name)" href="#" class="btn btn-danger btn_delete">x</a></td>
          </tr>
        </tbody>
        <tfoot></tfoot>
      </table>
    </div>

    <div>
      <RouterLink to="/animals/add" class="btn btn-success">Добавить</RouterLink>
    </div>
    <div class="mt-2">
      <RouterLink v-for="n in pagin_list" class="btn btn-primary mx-1" :class="{ activePagBtn: pagBtnIsActive(n) }"
        :to="`/animals/page/${n}`" :key="n">{{ n }}</RouterLink>
    </div>

<!--    <button id="show-modal" @click="showModal = true">Показать модальное окно</button>-->
    <Teleport to="body">
      <modal :show="showModal" @close="showModal = false">
        <template #header>
          <h3>Вы уверены?</h3>
        </template>
        <template #body>
          Действительно хотите удалить "{{ deleted_name }}"?
        </template>
        <template #footer>
          <button @click="showModal=false; confirm_delete=true; deleteAnimal(this.deleted_id)"
                  class="btn btn-danger btn_yes">Да</button>
          <button @click="showModal=false; resetDeleted()" class="btn btn-primary btn_no">Нет</button>
        </template>
      </modal>
    </Teleport>


    <Teleport to="body">
      <modal :show="showModalDelImpossible" @close="showModalDelImpossible = false">
        <template #header>
          <h3>Удаление невозможно</h3>
        </template>
        <template #body>
          {{ parent_delete_error }}
        </template>
        <template #footer>
          <button @click="showModalDelImpossible=false; " class="btn btn-primary btn_no">Ok</button>
        </template>
      </modal>
    </Teleport>

  </div>
</template>

<style scoped>

</style>