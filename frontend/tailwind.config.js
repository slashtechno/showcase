/** @type {import('tailwindcss').Config} */
import { themes } from "./src/lib/consts";
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
          primary: "#f68987",

          secondary: "#337d78",

          accent: "#F3D24F",

          neutral: "#fff536",

          "base-100": "#28615d",
          "base-200": "#1e4947",
          "base-300": "#183a38",

          info: "#00ffff",

          success: "#92ccf4",

          warning: "#fff536",

          error: "#e74b3c",
        },
      },
    ],
  },
};
