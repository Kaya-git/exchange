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
                            <v-list-item class="reviews-list__item">
                                <v-card class="reviews-list__card" rounded color="grey-lighten-3">
                                    <v-card-title class="reviews-list__title">
                                        Отзыв 1
                                    </v-card-title>
                                    <v-card-subtitle class="reviews-list__subtitle">
                                        05.11.2023
                                    </v-card-subtitle>
                                    <v-card-text class="reviews-list__text">
                                        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Incidunt, odio?
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                            <v-list-item class="reviews-list__item">
                                <v-card class="reviews-list__card" rounded color="grey-lighten-3">
                                    <v-card-title class="reviews-list__title">
                                        Отзыв 1
                                    </v-card-title>
                                    <v-card-subtitle class="reviews-list__subtitle">
                                        05.11.2023
                                    </v-card-subtitle>
                                    <v-card-text class="reviews-list__text">
                                        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Incidunt, odio?
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                            <v-list-item class="reviews-list__item">
                                <v-card class="reviews-list__card" rounded color="grey-lighten-3">
                                    <v-card-title class="reviews-list__title">
                                        Отзыв 1
                                    </v-card-title>
                                    <v-card-subtitle class="reviews-list__subtitle">
                                        05.11.2023
                                    </v-card-subtitle>
                                    <v-card-text class="reviews-list__text">
                                        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Incidunt, odio?
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                            <v-list-item class="reviews-list__item">
                                <v-card class="reviews-list__card" rounded color="grey-lighten-3">
                                    <v-card-title class="reviews-list__title">
                                        Отзыв 1
                                    </v-card-title>
                                    <v-card-subtitle class="reviews-list__subtitle">
                                        05.11.2023
                                    </v-card-subtitle>
                                    <v-card-text class="reviews-list__text">
                                        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Incidunt, odio?
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                            <v-list-item class="reviews-list__item">
                                <v-card class="reviews-list__card" rounded color="grey-lighten-3">
                                    <v-card-title class="reviews-list__title">
                                        Отзыв 1
                                    </v-card-title>
                                    <v-card-subtitle class="reviews-list__subtitle">
                                        05.11.2023
                                    </v-card-subtitle>
                                    <v-card-text class="reviews-list__text">
                                        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Incidunt, odio?
                                    </v-card-text>
                                </v-card>
                            </v-list-item>
                        </v-list>
                        <v-pagination 
                            class="mt-3"
                            :length="5" 
                            color="white"
                            :total-visible="2"
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
import {defineComponent, defineAsyncComponent} from 'vue';

export default defineComponent({
name: 'ReviewView',
    data: () => ({
        
    }),
    components: {
        ReviewModal: defineAsyncComponent({
            loader: () => import("../Modal/ReviewModal"),
        }),
    },
});
</script>
