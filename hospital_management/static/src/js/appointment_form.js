odoo.define('hospital_management.appointment_form', function(require){
"use strict";
var rpc = require('web.rpc');

 $('body').on('change','#patient_card',function(){
 var card = $('#patient_card').find(":selected").val();
     rpc.query({
          model:'hospital.management.appointment',
          method: 'patient_name',
          args: [,card],
     }).then(function(data){
     $('#patient_name').val(data);
     });
 });

 $('body').on('change','#doctor_name',function(event){
    var doctor = $(this).find(":selected").val();
    rpc.query({
        model:'hospital.management.appointment',
        method:'doctor_details',
        args:[,doctor],
    }).then(function(data){
    $('#doctor_department').val(data[0]);
    $('#doctor_fee').val(data[1]);
    })
 });
});
