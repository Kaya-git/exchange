<template>
    <div class="faq">
        <v-sheet class="faq__sheet" rounded>
            <div class="faq__content">
                <h1 class="faq__title title title_h1">
                    Вопросы и ответы
                </h1>
                <v-expansion-panels class="faq__panels faq-panels">
                    <v-expansion-panel
                        v-for="question in questions"
                        :key="question.id"
                        class="faq-panels__panel">
                        <v-expansion-panel-title class="faq-panels__title">
                            {{question.question}}
                        </v-expansion-panel-title>
                        <v-expansion-panel-text class="faq-panels__text">
                            {{question.answer}}
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
            </div>
        </v-sheet>
    </div>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'FaqView',

    data: () => ({
        questions: [],
    }),
    created() {
        this.getQuestions();
    },
    methods: {
        async getQuestions() {
            let response = await fetch('/api/faq/');
            if (response.ok && response.status === 200) {
                this.questions = await response.json();
            }
        }
    }
});
</script>
