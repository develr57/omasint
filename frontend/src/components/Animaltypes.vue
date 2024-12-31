<script>
import { mapActions, mapState } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../store/user';
import { useApiStore } from '../store/api';
import { useAnimaltypesStore } from "../store/animaltypes.js";
import { useRoutingStore } from "../store/routing.js";
import Modal from "./Modal.vue";
import moment from 'moment';



export default {
  name: "Animaltypes",
  components: {
    Modal,
  },
  data() {
    return {
      animaltypes: [],
      pagin_list: [],
      per_page: 10,
      start: null,
      end: null,
      showModal: false,
      confirm_delete: false,
      deleted_id: null,
      deleted_name: null,
      showModalDelImpossible: false,
      foreign_key_delete_error: null,
    }
  },
  computed: {
    ...mapState(useUserStore, [
      'token',
    ]),
    ...mapState(useApiStore, [
      'API_URL'
    ]),
    ...mapState(useAnimaltypesStore, [
        'getPageSize',
        'getTotalItems',
        'getCurrPage',
        'getOffset',
        'getTotalPages',
    ]),
    ...mapState(useRoutingStore, [
        'curr_route_name',
    ])
  },
  methods: {
    ...mapActions(useAnimaltypesStore, [
        'setPageSize',
        'setTotalItems',
        'setCurrPage',
        'setOffset',
        'setTotalPages'
    ]),
    ...mapActions(useRoutingStore, [
        'setCurrRouteName'
    ]),
    async getAnimalTypes() {
      const data = await axios.get(`${this.API_URL}/api/v1/animaltypes/`, {
        params: {
          limit: this.getPageSize,
          offset: this.getOffset,
        },
        headers: {
          Authorization: 'Token ' + this.token
        }
      }).then(resp => {
        console.log('resp: ', resp);
        this.animaltypes = resp.data.results;
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
      if (this.getTotalPages <= this.per_page) {
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
    async deleteAnimalType(id) {
      if (this.confirm_delete === true) {
        const data = await axios.delete(`${this.API_URL}/api/v1/animaltypes/${id}/`,{
          params: {},
          headers: {
            Authorization: 'Token ' + this.token
          }
        }).then(resp => {
          console.log('delete resp: ', resp);
          if (resp.status === 204) {
            this.getAnimalTypes();
          }
        }).catch(error => {
          console.log('delete error: ', error);
          if (error.status === 403 && error.response.data.detail) {
            this.foreign_key_delete_error = error.response.data.detail;
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
    returnDateAndTime(date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss');
    },
  },
  created() {
    this.setCurrPage(this.$route.params.page);
    this.setOffset((this.getCurrPage - 1) * this.getPageSize);
    this.getAnimalTypes();
    this.setCurrRouteName(this.$route.name);
    document.title = 'Типы животных';
  },
  watch: {
    '$route.params.page': function () {
      this.setCurrPage(this.$route.params.page);
      this.setOffset((this.getCurrPage - 1) * this.getPageSize);
      this.getAnimalTypes();
    }
  }
}
</script>


<template>
  <div>
    <h3 class="mt-4">Типы животных</h3>
    <div class="table-responsive mt-4">
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th scope="col">id</th>
            <th scope="col">Тип</th>
            <th scope="col">Создан</th>
            <th scope="col">Изменён</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="animaltype in animaltypes" :key="animaltype.id">
            <td>{{ animaltype.id }}</td>
            <td><RouterLink :to="`/animaltypes/edit/${animaltype.id}`">{{ animaltype.name }}</RouterLink></td>
            <td>{{ returnDateAndTime(animaltype.created_at) }}</td>
            <td>{{ returnDateAndTime(animaltype.updated_at) }}</td>
            <td><a @click="confirmationDelete(animaltype.id, animaltype.name)" href="#" class="btn">❌</a></td>
          </tr>
        </tbody>
        <tfoot></tfoot>
      </table>
    </div>
    <div>
      <RouterLink to="/animaltypes/add" class="btn btn-success">Добавить</RouterLink>
    </div>
    <div class="mt-2">
      <RouterLink v-for="n in pagin_list" class="btn btn-primary mx-1" :class="{ activePagBtn: pagBtnIsActive(n) }"
        :to="`/animaltypes/page/${n}`">{{ n }}</RouterLink>
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
          <button @click="showModal=false; confirm_delete=true; deleteAnimalType(this.deleted_id)"
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
          {{ foreign_key_delete_error }}
        </template>
        <template #footer>
          <button @click="showModalDelImpossible=false; " class="btn btn-primary btn_no">Ok</button>
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