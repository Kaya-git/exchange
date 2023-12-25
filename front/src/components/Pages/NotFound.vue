<template>
    <div class="not-found">
        <v-container fluid class="not-found__container">
            <div class="not-found__wrapper">
                <div class="not-found__content">
                    <div class="not-found__text">
                        <h2 class="not-found__title title title_h2">Страница не найдена</h2>
                        <p>Страница, которую вы ищете, не существует или была удалена</p>
                        <div class="not-found__btn">
                            <RouterLink to="/">
                                <v-btn size="large">На главную страницу</v-btn>
                            </RouterLink>
                        </div>
                    </div>
                    <div class="not-found__img">
                        <span class="not-found__img-text">404</span>
                    </div>
                </div>
            </div>
        </v-container>
    </div>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'NotFound',

    data: () => ({

    }),
});
</script>
