/** @type {import('tailwindcss').Config} */
import { themes } from "./src/lib/themes";
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Phantom Sans', 'sans-serif'],
      },
    },
  },

  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      ...themes,
      {
        scrapyard: {
          primary: "#91ccf4",

          secondary: "#F1A3BA",

          accent: "#F3D24F",

          neutral: "#47aea9",

          "base-100": "#337d78",
          "base-200": "1e4947",
          "base-300": "#183a38",

          info: "#00ffff",

          success: "#00ff00",

          warning: "#f59e0b",

          error: "#e11d48",
        },
      },
    ],
  },
};
