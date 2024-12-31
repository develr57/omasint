<script>
import { mapActions, mapState } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../store/user';
import { useApiStore } from '../store/api';


export default {
    name: "Register",
    data() {
        return {
            username: '',
            email: '',
            password: '',
            re_password: '',
            is_active: 0,
            username_valid_error: null,
            email_valid_error: null,
            password_valid_error: null,
            re_password_valid_error: null,
            other_error: null,
            rePassOk: false,
            reg_data: null,
        }
    },
    computed: {
        ...mapState(useApiStore, [
            'API_URL',
        ]),
    },
    methods: {
        async register() {
            const reg = await axios.post(`${this.API_URL}/api/v1/auth/users/`, {
                username: this.username,
                email: this.email,
                password: this.password,
                // is_active: this.is_active
            }).then(resp => {
                console.log('resp: ', resp.status);
                if (resp.status === 201) {
                    this.reg_data = resp.data;
                }
            }).catch(error => {
                console.log('error: ', error);
                if (error.response.data.username) {
                    this.username_valid_error = error.response.data.username[0];
                } else {
                    this.username_valid_error = null;
                }
                if (error.response.data.email) {
                    this.email_valid_error = error.response.data.email[0];
                } else {
                    this.email_valid_error = null;
                }
                if (error.response.data.password) {
                    this.password_valid_error = error.response.data.password[0];
                } else {
                    this.password_valid_error = null;
                }
                if (error.response.status == 400 && error.response.data[0]) {
                    this.other_error = error.response.data[0];
                }
            });
        },
        check() {
            this.username_valid_error = null;
            this.email_valid_error = null;
            this.password_valid_error = null;
            if (!this.re_password_valid_error) {
                this.register();
            }
        }
    },
    watch: {
        password: function() {
            if (this.password && this.re_password && this.password == this.re_password) {
                this.rePassOk = true;
                this.re_password_valid_error = null;
            } else {
                this.rePassOk = false;
                this.re_password_valid_error = 'Должно совпадать с полем "Пароль"!';
            }
        },
        re_password: function() {
            if (this.password && this.re_password && this.password == this.re_password) {
                this.rePassOk = true;
                this.re_password_valid_error = null;
            } else {
                this.rePassOk = false;
                this.re_password_valid_error = 'Должно совпадать с полем "Пароль"!';
            }
        }
    }
}
</script>



<template>
    <div class="pt-4">
        <div>
            <h4>Рестрация нового пользователя</h4>
        </div>
        <div class="pt-2" v-if="reg_data === null">
            <form @submit.prevent="check">
                <div class="row g-3 align-items-center pb-3">
                    <div class="col-sm-12 col-md-3 col-lg-2">
                        <label for="inputUsername" class="col-form-label">Имя пользователя</label>
                    </div>
                    <div class="col-sm-12 col-md-5 col-lg-4">
                        <input v-model.trim="username" type="text" id="inputUsername" class="form-control"
                             aria-labelledby="usernameHelpInline">
                    </div>
                    <div class="col-sm-12 col-md-4 col-lg-6">
                        <span id="usernameHelpInline" class="form-text" v-if="username_valid_error === null">
                        Должно быть уникальным. С этим именем вы будете входить.
                        </span>
                        <span id="usernameHelpInline" class="form-text text-danger" v-if="username_valid_error !== null">
                            {{ username_valid_error }}
                        </span>
                    </div>
                </div>
                <div class="row g-3 align-items-center pb-3">
                    <div class="col-sm-12 col-md-3 col-lg-2">
                        <label for="emailPassword6" class="col-form-label">E-mail</label>
                    </div>
                    <div class="col-sm-12 col-md-5 col-lg-4">
                        <input v-model.trim="email" type="text" id="inputEmail" class="form-control" aria-labelledby="emailHelpInline">
                    </div>
                    <div class="col-sm-12 col-md-4 col-lg-6">
                        <span id="emailHelpInline" class="form-text" v-if="email_valid_error === null">
                            Ваша электронная почта
                        </span>
                        <span id="emailHelpInline" class="form-text text-danger" v-if="email_valid_error !== null">
                            {{ email_valid_error }}
                        </span>
                    </div>
                </div>
                <div class="row g-3 align-items-center pb-3">
                    <div class="col-sm-12 col-md-3 col-lg-2">
                        <label for="inputPassword" class="col-form-label">Пароль</label>
                    </div>
                    <div class="col-sm-12 col-md-5 col-lg-4">
                        <input v-model.trim="password" type="password" id="inputPassword" class="form-control"
                             aria-labelledby="passwordHelpInline" autocomplete="off">
                    </div>
                    <div class="col-sm-12 col-md-4 col-lg-6">
                        <span id="passwordHelpInline" class="form-text" v-if="password_valid_error === null">
                            Должно быть от 8 символов. 
                        </span>
                        <span id="passwordHelpInline" class="form-text text-danger" v-if="password_valid_error !== null">
                            {{ password_valid_error }}
                        </span>
                    </div>
                </div>
                <div class="row g-3 align-items-center pb-4">
                    <div class="col-sm-12 col-md-3 col-lg-2">
                        <label for="inputRePassword" class="col-form-label">Повторить пароль</label>
                    </div>
                    <div class="col-sm-12 col-md-5 col-lg-4">
                        <input v-model.trim="re_password" type="password" id="inputRePassword" class="form-control"
                               aria-labelledby="rePasswordHelpInline" autocomplete="off">
                    </div>
                    <div class="col-sm-12 col-md-4 col-lg-6">
                        <span id="rePasswordHelpInLine" class="text-success fw-bold fs-4 px-2" v-if="rePassOk">✓</span>
                        <span id="rePasswordHelpInLine" class="text-danger fw-bold fs-4 px-2" v-if="re_password_valid_error !== null">❌</span>
                        <span id="rePasswordHelpInline" class="form-text" v-if="re_password_valid_error === null && rePassOk === false">
                            Должно совпадать с полем "Пароль".
                        </span>
                        <span id="rePasswordHelpInline" class="form-text text-danger" v-if="re_password_valid_error !== null">
                            {{ re_password_valid_error }}
                        </span>
                    </div>
                </div>
                <p class="text-danger" v-if="other_error">{{ other_error }}</p>
                <button type="submit" class="btn btn-primary ms-5">Отправить</button>
            </form>
        </div>
        <div v-if="reg_data !== null" class="pt-2">
            <div class="row">
                <p>Регистрация прошла успешно!</p>
                <p class="text-break">На электронную почту {{ reg_data.email }} отправлена ссылка. Вам нужно перейти по этой ссылке 
                    для активации вашего аккаунта. В противном случае Вы не сможете авторизоваться.</p>
            </div>
        </div>
    </div>
</template>



<style>
</style>