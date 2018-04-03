<template>
    <div>
        <div class="row" v-if="sortedItems.length > 0">
            <div class="col-6 col-md-3 g-mb-30" v-for="item in sortedItems">
                <gallery-item
                        :id="item.id"
                        :imgSm="item.img_sm"
                        :imgLg="item.img_lg"
                        :likesCount="item.likes_count"
                        :canLike="item.can_like"
                        @incLikes="incLikes(item.id)"
                />
            </div>
        </div>
        <div class="row" v-else>
            <div class="col-12 text-center g-font-size-18 g-font-weight-600">
                <p v-if="busy">Загрузка фотографий...</p>
                <p v-else>Фотографии пока что отсутствуют.</p>
            </div>
        </div>
    </div>
</template>

<script>
    import GalleryItem from './GalleryItem.vue';
    import axios from '../config-axios';

    export default {
        name: "gallery",
        components: {
            GalleryItem: GalleryItem,
        },
        props: ['eventId'],
        data() {
            return {
                items: [],
                itemsPerPage: 16,
                page: 1,
                busy: true
            }
        },
        computed:{
            sortedItems () {
                return this.items.sort(function(a, b) {
                    return b.likes_count - a.likes_count;
                }).slice(0, this.page * this.itemsPerPage);
            }
        },
        methods: {
            load() {
                axios.get('/photo-archive/photos.json?event_id=' + this.eventId)
                    .then((response) => {
                        this.items = response.data;
                        this.busy = false;
                    }).catch(function (error) {
                        console.log(error);
                    });
            },
            incLikes(id) {
                let item = this.items.find(x => x.id === id);
                item.likes_count++;
                item.can_like = false;
            },
            onScroll() {
                if ($(window).height() + $(window).scrollTop() >= $(document).height() - $("#footer").height()
                    && this.pageCount > this.page && !this.busy) {
                    this.page++;
                }
            }
        },
        created() {
            window.addEventListener('scroll', this.onScroll);
            this.load();
            this.pageCount = Math.ceil(this.items.length / this.itemsPerPage);
        }
    }
</script>

<style scoped>

</style>