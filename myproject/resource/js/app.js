require('./bootstrap');

import 'select2';                       // globally assign select2 fn to $ element  // optional if you have css loader
import Chart from 'chart.js'
require('bootstrap-datepicker/js/bootstrap-datepicker.js');
require( 'datatables.net-buttons-bs4' )( $ );
$(() => {
  $('.select2-enable').select2();
});
import Swal from 'sweetalert2'

window.Swal = Swal;

var dt = require('datatables.net-bs4');

window.$.DataTable = dt;