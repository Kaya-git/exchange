<template>
  <v-dialog
      width="auto"
      persistent
      class="confirm-modal align-center justify-center">
      <v-sheet
          class="confirm-modal__sheet pa-4"
          rounded>
        <v-container fluid class="confirm-modal__container">
          <v-row class="justify-center">
            <div class="confirm-modal__cardnumber">
              <div class="confirm-modal__cardnumber-wrapper">
                <span>3243 4545 4757 5456 Денис Н.</span>
              </div>
            </div>
          </v-row>
          <v-row class="justify-center">
            <p class="confirm-modal__text">Подтвердите перевод по указанным <br> выше реквизитам</p>
          </v-row>
          <v-row>
            <v-col class="d-flex justify-end">
              <v-btn size="large" color="success" @click="confirmTrade()">
                Оплачено
              </v-btn>
            </v-col>
            <v-col>
                <v-btn size="large" color="error" @click="toggleConfirmOverlay()">Вернуться</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-sheet>
  </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import { mapGetters, mapMutations } from 'vuex';

export default defineComponent({
  name: 'ConfirmTrade',
  data: () => ({
  }),
  mounted() {

  },
  methods: {
    ...mapMutations ([
      'toggleWaitOverlay',
      'toggleConfirmOverlay'
    ]),
    async confirmTrade() {
      this.toggleWaitOverlay();
      let response = await fetch('/api/exchange/confirm_button');
      if (response.ok) {
        // let result = await response.json();
      }
    }
  },
  computed: {
    ...mapGetters([
      'getWaitOverlayState',
      'getConfirmOverlayState'
    ]),
  }
});
</script>
