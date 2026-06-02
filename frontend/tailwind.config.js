/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // Radi omogucavanja tamne tematike na dijelu za forum
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ff7a00',
        secondary: '#ffb380',
      }
    },
  },
  plugins: [],
}