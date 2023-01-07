odoo.define('hospital_snippet.doctor_snippet', function (require) {
    var core = require('web.core');
    var QWeb = core.qweb;
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    var Dynamic = PublicWidget.Widget.extend({
       selector: '.top4_doctors',

       willStart: async function () {
           await rpc.query({
               route: '/top4/doctors',
           }).then((result)  =>{
              this.result=result;
           })
       },

       start: function(){
            var chunks = _.chunk(this.result, 4)
            chunks[0].is_active = true
            this.$el.find('#doctors').html(
                QWeb.render('hospital_management.qweb_doctor_carousal',{chunks})
            )
       },

   });
   PublicWidget.registry.top4_doctors = Dynamic;
   return Dynamic;
});



       start: function () {
           var self = this;
           rpc.query({
               route: '/top4/doctors',
               params: {},
           }).then(function (result) {
               self.$('#div1').html(result);
           });
       },

