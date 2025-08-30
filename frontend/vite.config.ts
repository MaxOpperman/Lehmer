import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue()],
  define: {
    __APP_VERSION__: JSON.stringify("v1.0.0"),
  },
});
