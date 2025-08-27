interface RuntimeConfig {
  VITE_API_URL: string;
  FRONTEND_PORT: string;
  [key: string]: string; // Allow additional dynamic properties
}

const RUNTIME_CONFIG: RuntimeConfig = {
  VITE_API_URL: import.meta.env.VITE_API_URL || "http://localhost:5050",
  FRONTEND_PORT: import.meta.env.FRONTEND_PORT || "5173",
};

export default RUNTIME_CONFIG;