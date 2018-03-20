<template>
    <div>
        <div v-if="serverErrors && serverErrors.length" class="alert alert-danger fade show g-mb-20" role="alert">
            <h4 class="h5">
                <i class="fa fa-minus-circle"></i>
                Обнаружены ошибки!
            </h4>
            <ul class="u-alert-list g-mt-10">
                <li v-for="(error, index) in serverErrors" :key="index">{{error.message}}</li>
            </ul>
        </div>

        <form @submit.prevent="sendData" v-if="!sended" role="form">
            <div class="row">
                <div class="col-md-6">

                    <div :class="{'u-has-error-v1': errors.has('last_name') }" class="form-group">
                        <div class="input-group g-brd-primary--focus g-rounded-3 g-mb-0--md">
                            <input class="form-control"
                                   name="last_name"
                                   v-validate="'required'"
                                   data-vv-as="Фамилия юного зрителя"
                                   v-model="last_name"
                                   :disabled="processing"
                                   placeholder="Фамилия юного зрителя"
                                   type="text"
                            >
                            <div class="input-group-append">
                                <span class="input-group-text"><i class="fa fa-user"></i></span>
                            </div>
                        </div>
                        <small v-show="errors.has('last_name')"
                               class="form-control-feedback g-pl-5"
                        >{{ errors.first('last_name') }}</small>
                    </div>

                    <div :class="{'u-has-error-v1': errors.has('first_name') }" class="form-group">
                        <div class="input-group g-brd-primary--focus g-rounded-3 g-mb-0--md">
                            <input class="form-control"
                                   name="first_name"
                                   v-validate="'required'"
                                   data-vv-as="Имя юного зрителя"
                                   v-model="first_name"
                                   :disabled="processing"
                                   placeholder="Имя юного зрителя"
                                   type="text"
                            >
                            <div class="input-group-append">
                                <span class="input-group-text"><i class="fa fa-user"></i></span>
                            </div>
                        </div>
                        <small v-show="errors.has('first_name')"
                               class="form-control-feedback g-pl-5"
                        >{{ errors.first('first_name') }}</small>
                    </div>

                    <div :class="{'u-has-error-v1': errors.has('patronymic_name') }" class="form-group">
                        <div class="input-group g-brd-primary--focus g-rounded-3 g-mb-0--md">
                            <input class="form-control"
                                   name="patronymic_name"
                                   v-validate="'required'"
                                   data-vv-as="Отчество юного зрителя"
                                   v-model="patronymic_name"
                                   :disabled="processing"
                                   placeholder="Отчество юного зрителя"
                                   type="text"
                            >
                            <div class="input-group-append">
                                <span class="input-group-text"><i class="fa fa-user"></i></span>
                            </div>
                        </div>
                        <small v-show="errors.has('patronymic_name')"
                               class="form-control-feedback g-pl-5"
                        >{{ errors.first('patronymic_name') }}</small>
                    </div>

                </div>
                <div class="col-md-6">
                    <div :class="{'u-has-error-v1': errors.has('phone')}" class="form-group">
                        <div class="input-group g-brd-primary--focus g-rounded-3 g-mb-0--md">
                            <input class="form-control"
                                   name="phone"
                                   v-validate="'required'"
                                   data-vv-as="Ваш телефон"
                                   v-model="phone"
                                   :disabled="processing"
                                   placeholder="Ваш телефон"
                                   type="text"
                            >
                            <div class="input-group-append">
                                <span class="input-group-text"><i class="fa fa-phone"></i></span>
                            </div>
                        </div>
                        <small v-show="errors.has('phone')"
                               class="form-control-feedback g-pl-5"
                        >{{ errors.first('phone') }}</small>
                    </div>

                    <div :class="{'u-has-error-v1': errors.has('email')}" class="form-group ">
                        <div class="input-group g-brd-primary--focus g-rounded-3 g-mb-0--md">
                            <input class="form-control"
                                   name="email"
                                   v-validate="'required|email'"
                                   data-vv-as="Ваш E-Mail"
                                   v-model="email"
                                   :disabled="processing"
                                   placeholder="Ваш E-Mail"
                                   type="email">
                            <div class="input-group-append">
                                <span class="input-group-text"><i class="fa fa-envelope-o"></i></span>
                            </div>
                        </div>
                        <small v-show="errors.has('email')"
                               class="form-control-feedback"
                        >{{ errors.first('email') }}</small>
                    </div>
                </div>
            </div>

            <div class="row justify-content-center g-mt-20">
                <div class="col-md-3">
                    <button class="btn btn-block btn-md u-btn-primary text-uppercase g-font-size-14 g-font-weight-600 g-rounded-5 g-py-12"
                            :disabled="processing"
                            type="submit">Зарегистрироваться
                    </button>
                </div>
            </div>
        </form>
        <p class="g-font-size-16 text-center" v-else>Спасибо, вы успешно зарегистрированы. Также на ваш E-Mail отправлено письмо с данными о мероприятии.</p>
    </div>
</template>

<script>
    import axios from '../config-axios';
    import qs from 'qs';

    export default {
        name: "event-registration-form",
        props: ['event_id'],
        data() {
            return {
                first_name: '',
                last_name: '',
                patronymic_name: '',
                email: '',
                phone: '',
                sended: false,
                processing: false,
                serverErrors: []
            }
        },
        methods: {
            sendData() {

                this.serverErrors = [];

                this.$validator.validateAll().then(result => {
                    if (result) {
                        this.processing = true;

                        axios.post('', qs.stringify({
                            first_name: this.first_name,
                            last_name: this.last_name,
                            patronymic_name: this.patronymic_name,
                            email: this.email,
                            phone: this.phone,
                        }))
                            .then(() => {
                                this.serverErrors = [];
                                this.sended = true;
                                this.processing = false;
                            })
                            .catch(e => {
                                this.serverErrors.push(e);
                                this.processing = false;
                            });
                    }
                });
            }
        }
    }
</script>

<style scoped>

</style>