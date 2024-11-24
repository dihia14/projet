/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js,py}", 
    "./static/**/*.{css,js}",       
    "./app/app.py"     ,               
  ],  theme: {
    extend: {},
  },
  plugins: [],
}
