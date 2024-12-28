/** @type {import('tailwindcss').Config} */
import {themes} from './src/lib/themes';
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  darkMode: ["class"],

  theme: {
    extend: {
      },
    },

    plugins: [require('@tailwindcss/typography'), require('daisyui')],
    daisyui: {
      themes: themes,
    }
};
