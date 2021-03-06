import "babel-polyfill";
import Vue from 'vue';
import { yandexMap, ymapMarker } from 'vue-yandex-maps'
import VeeValidate, {Validator} from 'vee-validate';
import ru from 'vee-validate/dist/locale/ru';

Validator.localize('ru', ru);
Vue.use(VeeValidate, {
    locale: 'ru'
});

import ContactForm from './vue-components/ContactForm.vue';
import EventRegistrationForm from './vue-components/EventRegistrationForm.vue';
import Gallery from './vue-components/Gallery.vue';

new Vue({
    el: '#app',
    components: {
        yandexMap,
        ymapMarker,
        ContactForm: ContactForm,
        EventRegistrationForm: EventRegistrationForm,
        Gallery: Gallery,
    }
});