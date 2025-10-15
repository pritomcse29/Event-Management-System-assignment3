// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     "./templates/**/*.html", // Templates at the project level
//     "./**/templates/**/*.html", // Templates inside apps  
//   ],
//   theme: {
//     extend: {
     
//     },
//   },
//   plugins: [],
// }

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  "./templates/**/*.html", // Templates at the project level
    "./**/templates/**/*.html", // Templates inside apps  
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],

  daisyui: {
    themes: ["light", "dark", "corporate", "synthwave", "dracula", "lemonade"], // Include themes you might want to switch between
    // You can set a default theme if you want, e.g., defaultTheme: "corporate",
  },
}