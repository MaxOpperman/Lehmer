import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue()],
  define: {
    __APP_VERSION__: JSON.stringify("v1.0.0"),
    "import.meta.env.VITE_API_URL": JSON.stringify(process.env.VITE_API_URL || "http://localhost:5050"),
    "import.meta.env.FRONTEND_PORT": JSON.stringify(process.env.FRONTEND_PORT || "5173"),
  },
});