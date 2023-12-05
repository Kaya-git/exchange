<template>
  <v-dialog
      width="auto"
      class="wait-modal align-center justify-center">
      <v-sheet
          v-if="isActive"
          class="wait-modal__sheet pa-4"
          rounded>
        <v-container fluid class="wait-modal__container">
          <v-row>

          </v-row>
          <v-row>
            <v-col class="d-flex justify-end">
              <v-btn id="request-submit" size="large" color="success" @click="toggleWaitOverlay()">
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
  props: {
    isActive: {
        type: Boolean,
        default: false,
    }
  },
  data: () => ({
  }),
  mounted() {

  },
  methods: {
    ...mapMutations ([
      'toggleWaitOverlay',
      'toggleConfirmOverlay'
    ]),
  },
  computed: {
    ...mapGetters([
      'getWaitOverlayState',
      'getConfirmOverlayState'
    ]),
  }
});
</script>
