import { createApp } from "vue";
import PrimeVue from "primevue/config";
import ToastService from "primevue/toastservice";
import "primeicons/primeicons.css";
import Lara from "./presets/lara";

import "./style.css";
import App from "./App.vue";

const app = createApp(App);
app.use(PrimeVue, {
  unstyled: false,
  ripple: true,
  pt: Lara,
});
app.use(ToastService);
app.mount("#app");
