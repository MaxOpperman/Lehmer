import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  define: {
    __APP_VERSION__: JSON.stringify('v1.0.0'),
    __API_URL__: JSON.stringify('http://lehmer_backend:5050'),
  },
});
