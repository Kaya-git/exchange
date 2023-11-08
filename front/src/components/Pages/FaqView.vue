<template>
    <div class="faq">
        <v-sheet class="faq__sheet" rounded>
            <div class="faq__content">
                <h1 class="faq__title title title_h1">
                    Вопросы и ответы
                </h1>
                <v-expansion-panels class="faq__panels faq-panels">
                    <v-expansion-panel class="faq-panels__panel">
                        <v-expansion-panel-title class="faq-panels__title">
                            Вопрос 1
                        </v-expansion-panel-title>
                        <v-expansion-panel-text class="faq-panels__text">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad tempore rerum quos qui doloremque esse necessitatibus tempora nemo? Autem, vel?
                        </v-expansion-panel-text>  
                    </v-expansion-panel>
                    <v-expansion-panel class="faq-panels__panel">
                        <v-expansion-panel-title class="faq-panels__title">
                            Вопрос 2
                        </v-expansion-panel-title>
                        <v-expansion-panel-text class="faq-panels__text">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad tempore rerum quos qui doloremque esse necessitatibus tempora nemo? Autem, vel?
                        </v-expansion-panel-text>  
                    </v-expansion-panel>
                    <v-expansion-panel class="faq-panels__panel">
                        <v-expansion-panel-title class="faq-panels__title">
                            Вопрос 3
                        </v-expansion-panel-title>
                        <v-expansion-panel-text class="faq-panels__text">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad tempore rerum quos qui doloremque esse necessitatibus tempora nemo? Autem, vel?
                        </v-expansion-panel-text>  
                    </v-expansion-panel>
                    <v-expansion-panel class="faq-panels__panel">
                        <v-expansion-panel-title class="faq-panels__title">
                            Вопрос 4
                        </v-expansion-panel-title>
                        <v-expansion-panel-text class="faq-panels__text">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad tempore rerum quos qui doloremque esse necessitatibus tempora nemo? Autem, vel?
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
    
}),
});
</script>
