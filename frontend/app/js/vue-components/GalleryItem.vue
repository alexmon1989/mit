<template>
    <article class="u-block-hover g-rounded-6">
        <figure class="u-bg-overlay g-bg-black-opacity-0_2--after">
            <img class="img-fluid u-block-hover__main--zoom-v1" :src="imgSm" alt="">
        </figure>
        <div v-if="canLike" class="u-bg-overlay__inner g-absolute-centered">
            <a @click.prevent="like" href="#!" class="btn btn-lg u-btn-primary">
                <i class="fa fa-thumbs-up"></i>
            </a>
        </div>
        <ul class="list-inline u-bg-overlay__inner g-pos-abs g-bottom-0 g-left-10 g-opacity-0_8">
            <li class="list-inline-item" :class="classObject">
                <i class="fa fa-thumbs-up g-font-size-18" aria-hidden="true"></i> {{ likesCount }}
            </li>
        </ul>
        <a class="js-fancybox u-link-v2"
           href="javascript:;"
           data-fancybox="lightbox-gallery--05"
           :data-src="imgLg">Read More
        </a>
    </article>
</template>

<script>
    import axios from '../config-axios';
    import qs from 'qs';

    export default {
        props: ['id', 'imgSm', 'imgLg', 'likesCount', 'canLike'],
        name: "gallery-item",
        computed: {
            classObject: function () {
                return {
                    'g-color-primary': !this.canLike,
                    'g-color-white': this.canLike,
                }
            }
        },
        methods: {
            like() {
                axios.post('/photo-archive/like/', qs.stringify({ id: this.id }))
                    .then(() => {
                        this.$emit('incLikes', this.id)
                    }).catch(function (error) {
                    console.log(error);
                });
            }
        }
    }
</script>

<style scoped>

</style>