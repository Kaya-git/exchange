<template>
    <v-dialog
        max-width="800"
        persistent
        class="verification-modal align-center justify-center">
        <v-sheet
            class="verification-modal__sheet pa-4"
            rounded>
            <v-container fluid class="verification-modal__container">
                <v-form validate-on="submit lazy" @submit.prevent="confirm">
                    <v-row class="justify-center">
                        <h2 class="verification-modal__title title title_h2 title_black mb-4">Верификация карты</h2>
                    </v-row>
                    <v-row class="justify-center">
                        <p class="verification-modal__text">{{ msg }}</p>
                    </v-row>
                    <v-row class="justify-center">
                        <div class="verification-modal__file-input-wrapper">
                            <v-file-input
                                v-model="file"
                                :rules="fileRules"
                                show-size
                                accept="image/png, image/jpeg"
                                prepend-icon="mdi-camera"
                                label="Загрузите фото">
                            </v-file-input>
                            <span class="verification-modal__file-caption">*размер фото не более 8 МБ</span>
                        </div>
                    </v-row>
                    <v-row>
                        <p class="verification-modal__text verification-modal__instruction-title">Для верификации нажмите на инструкцию</p>
                        <v-expansion-panels>
                            <v-expansion-panel>
                                <v-expansion-panel-title>
                                    Верификация пластиковой карты
                                </v-expansion-panel-title>
                                <v-expansion-panel-text>
                                    <p class="verification-modal__text">
                                        <span class="verification-modal__prepend-icon">#</span>
                                        Пройдите простую одноразовую верификацию. Выберите удобный способ и следуйте инструкциям:
                                    </p>
                                    <v-divider class="border-opacity-75 my-2" color="cyan-lighten-3"></v-divider>
                                    <ul>
                                        <li v-for="(way, index) in ways.plastic" :key="'way-plastic-' + index">
                                            <v-chip class="verification-modal__chip" color="cyan-lighten-3" variant="flat">Способ {{index + 1}}</v-chip>
                                            <p class="verification-modal__text">
                                                {{way.text}}
                                            </p>
                                            <div @click.stop="openImgPreview" class="verification-modal__verify-example-wrapper verify-example-wrapper-parent mt-2">
                                                <span class="verification-modal__verify-example mr-1">
                                                    Смотреть образец ->
                                                </span>
                                                <span class="verification-modal__img-preview">
                                                    <img :src="way.img.src" :alt="way.img.alt">
                                                </span>
                                            </div>
                                            <v-divider class="border-opacity-75 my-2" color="cyan-lighten-3"></v-divider>
                                        </li>
                                    </ul>
                                </v-expansion-panel-text>
                            </v-expansion-panel>
                            <v-expansion-panel>
                                <v-expansion-panel-title>
                                    Верификация виртуальной карты
                                </v-expansion-panel-title>
                                <v-expansion-panel-text>
                                    <p class="verification-modal__text">
                                        <span class="verification-modal__prepend-icon">#</span>
                                        Пройдите простую одноразовую верификацию. Выберите удобный способ и следуйте инструкциям:
                                    </p>
                                    <ul>
                                        <li v-for="(way, index) in ways.virtual" :key="'way-virtual-' + index">
                                            <v-chip class="verification-modal__chip" color="cyan-lighten-3" variant="flat">Способ {{index + 1}}</v-chip>
                                            <p class="verification-modal__text">
                                                {{way.text}}
                                            </p>
                                            <div @click.stop="openImgPreview" class="verification-modal__verify-example-wrapper verify-example-wrapper-parent mt-2">
                                                <span class="verification-modal__verify-example mr-1">
                                                    Смотреть образец ->
                                                </span>
                                                <span class="verification-modal__img-preview">
                                                    <img :src="way.img.src" :alt="way.img.alt">
                                                </span>
                                            </div>
                                            <v-divider class="border-opacity-75 my-2" color="cyan-lighten-3"></v-divider>
                                        </li>
                                    </ul>
                                </v-expansion-panel-text>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-row>
                    <v-row>
                        <v-checkbox
                            v-model="checkVerifyRules.value"
                            :rules="[rules.required]"
                            :error="checkVerifyRules.error"
                            hide-details>
                            <template v-slot:label>
                                <div>
                                    Я ознакомился с правилами верификации карт
                                </div>
                            </template>
                        </v-checkbox>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex justify-center justify-sm-end">
                            <v-btn size="large" color="success" type="submit" :loading="loading || loader" :disabled="loading || loader">
                                {{ successMsg }}
                            </v-btn>
                        </v-col>
                        <v-col class="d-flex justify-center justify-sm-start">
                            <v-btn
                                size="large"
                                width="150"
                                color="error"
                                :disabled="loading || loader"
                                @click="$emit('canceled')">{{ rejectMsg }}
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import {mapMutations} from 'vuex';
import { v3ImgPreviewFn } from 'v3-img-preview';

export default defineComponent({
    name: 'VerificationModal',
    props: {
        msg: {
            type: String,
            default: '',
        },
        successMsg: {
            type: String,
            default: 'Отправить',
        },
        rejectMsg: {
            type: String,
            default: 'Отмена',
        },
        loader: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['confirmed', 'canceled'],
    data: () => ({
        file: null,
        checkVerifyRules: {
            value: false,
            error: false,
        },
        fileRules: [
            v => !!v || 'Обязательное поле',
            v => !!v.length || 'Пустой файл!',
            v => v[0].size < 8000000 || 'Превышен размер фото!',
            v => v[0].type === "image/png" || v[0].type === "image/jpeg" || "Разрешены только jpg, jpeg или png",
        ],
        rules: {
          required: v => !!v || 'Обязательное поле',
        },
        loading: false,
        verificationModal: null,
        ways: {
            plastic: [
                {
                    text: "Ознакомьтесь с образцом. Сфотографируйте экран приложения банка на фоне этой страницы, чтобы был виден логотип VVS Coin,\n" +
                        "а также первые 4 цифры и последние 4 цифры номера карты.",
                    img: {
                        src: "/img/image.jpg",
                        alt: "",
                    }
                },
                {
                    text: "ещё текст",
                    img: {
                        src: "/img/image.png",
                        alt: "",
                    }
                }
            ],
            virtual: [

            ]
        }
    }),
    mounted() {
    },
    methods: {
        ...mapMutations([
            'setVerificationFile',
        ]),
        async confirm(event) {
            this.loading = true;
            const results = await event;
            if (results.valid) {
                this.setVerificationFile(this.file[0]);
                this.$emit('confirmed');
            } else {
                this.checkVerifyRules.error = !this.checkVerifyRules.value;
            }
            this.loading = false;
        },
        openImgPreview(event) {
            this.verificationModal = document.querySelector(".verification-modal");
            v3ImgPreviewFn(event.target.closest(".verify-example-wrapper-parent").querySelector("img").src);
            if (this.verificationModal) this.verificationModal.style.zIndex = "1";
        }
    },
    computed: {
        isImgPreviewOpen() {
            const imgPreview = document.querySelector("#v3-img-preview-container-id");
            return imgPreview.innerHTML.trim() !== "";
        }
    }
});
</script>
