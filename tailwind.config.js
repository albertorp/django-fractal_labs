module.exports = {
  content: [
    './apps/**/*.html',
    './assets/**/*.js',
    './assets/**/*.ts',
    './assets/**/*.jsx',
    './assets/**/*.tsx',
    './assets/**/*.vue',
    './templates/**/*.html',
    './apps/web/templatetags/form_tags.py',
    './node_modules/flowbite/**/*.js',
  ],
  safelist: [
    'alert-success',
    'alert-info',
    'alert-error',
    'alert-warning',
    'pg-bg-danger',
    'pg-bg-success',
  ],
  theme: {
    extend: {
      aspectRatio: {
        '3/2': '3 / 2',
      },
      colors: {
        primary: {"50":"#eff6ff","100":"#dbeafe","200":"#bfdbfe","300":"#93c5fd","400":"#60a5fa","500":"#3b82f6","600":"#2563eb","700":"#1d4ed8","800":"#1e40af","900":"#1e3a8a","950":"#172554"}
      },
    },
    container: {
      center: true,
      // padding: '2rem',
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require("daisyui"),
    require('flowbite/plugin'),
  ],
}
