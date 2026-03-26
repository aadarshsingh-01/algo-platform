import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#0a0f1c",
        surface: "#111a2e",
        border: "#25314d",
        primary: "#22d3ee",
        success: "#10b981",
        danger: "#ef4444"
      }
    }
  },
  plugins: []
};

export default config;
