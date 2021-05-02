let mix = require('laravel-mix');

let staticPath = 'myproject/static/'
let resourcesPath = 'myproject/resource/'

mix.setResourceRoot('/static/') // setResroucesRoots add prefix to url() in scss on example: from /images/close.svg to /static/images/close.svg

mix.setPublicPath('myproject/static/') // Path where mix-manifest.json is created

// // if you don't need browser-sync feature you can remove this lines
// if (process.argv.includes('--browser-sync')) {
//   mix.browserSync('localhost:8000')
// }

// Now you can use full mix api
mix.js(`${resourcesPath}/js/app.js`, `${staticPath}/js/`)
mix.sass(`${resourcesPath}/sass/app.scss`, `${staticPath}/sass/`)