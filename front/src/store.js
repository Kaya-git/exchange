import Vuex from 'vuex';

export default new Vuex.Store({
    state: {
      exchangeData: null,
      waitOverlay: false,
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
      }
    },
    getters: {
      getExchangeData: state => state.exchangeData,
      getWaitOverlayState: state => state.waitOverlay,
    }
});