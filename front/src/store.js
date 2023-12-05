import Vuex from 'vuex';

export default new Vuex.Store({
    state: {
      exchangeData: null,
      waitOverlay: false,
      confirmOverlay: false,
    },
    mutations: {
      setExchangeData(state, data) {
        state.exchangeData = data;
      },
      openWaitOverlay(state) {
        state.waitOverlay = true;
      },
      closeWaitOverlay(state) {
        state.waitOverlay = false;
      },
      toggleWaitOverlay(state) {
        state.waitOverlay = !state.waitOverlay;
      },
      openConfirmOverlay(state) {
        state.confirmOverlay = true;
      },
      closeConfirmOverlay(state) {
        state.confirmOverlay = false;
      },
      toggleConfirmOverlay(state) {
        state.confirmOverlay = !state.confirmOverlay;
      }
    },
    getters: {
      getExchangeData: state => state.exchangeData,
      getWaitOverlayState: state => state.waitOverlay,
      getConfirmOverlayState: state => state.confirmOverlay,
    }
});