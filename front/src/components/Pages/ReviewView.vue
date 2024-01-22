<template>
    <div class="reviews">
        <v-sheet rounded class="reviews__sheet">
            <v-container fluid class="reviews__content">
                <v-row class="reviews__row">
                    <v-col class="reviews__col">
                        <h1 class="reviews__title title title_h1">
                            Отзывы наших клиентов
                        </h1>
                        <v-list rounded class="reviews__list reviews-list">
                            <v-list-item
                                class="reviews-list__item"
                                v-for="(review, i) in curReviews"
                                :key="i">
                                <v-card class="reviews-list__card" rounded color="grey-lighten-3">
                                    <v-card-title class="reviews-list__title">
                                        {{review.name}}
                                    </v-card-title>
                                    <v-card-subtitle class="reviews-list__subtitle">
                                        05.11.2023
                                    </v-card-subtitle>
                                    <v-card-text class="reviews-list__text">
                                        {{review.text}}
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                        </v-list>
                        <v-pagination 
                            class="mt-3"
                            :length="Math.ceil(reviews.length / reviewsPerPage)"
                            color="white"
                            :total-visible="2"
                            v-model="page"
                        >
                        </v-pagination>
                        <div class="reviews__bottom">
                            <review-modal ></review-modal>
                        </div>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
</template>

<script>
import {defineComponent, defineAsyncComponent, reactive} from 'vue';
import {mapActions} from 'vuex';

export default defineComponent({
name: 'ReviewView',
    data: () => ({
        reviews: reactive([]),
        page: 1,
        reviewsPerPage: 5,
    }),
    created() {
        this.getReviews();
    },
    mounted() {

    },
    components: {
        ReviewModal: defineAsyncComponent({
            loader: () => import("../Modal/ReviewModal"),
        }),
    },
    methods: {
        ...mapActions([
            'resizeBg',
        ]),
        async getReviews() {
            let response = await fetch('/api/reviews/list');
            if (response.ok && response.status === 200) {
                this.reviews = await response.json();
            }
            await this.$nextTick();
            this.resizeBg();
        }
    },
    computed: {
        curReviews() {
            return this.reviews.slice((this.page - 1) * this.reviewsPerPage, this.page * this.reviewsPerPage);
        }
    }
});
</script>
