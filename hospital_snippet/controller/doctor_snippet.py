from odoo import http
from odoo.http import request


class DoctorSnippet(http.Controller):
    @http.route(['/top4/doctors'], type="json", auth="public")
    def top4_doctors(self):
        # top4 = request.env['hr.employee'].search([('is_doctor', '=', True)], limit=4, order='op_count desc')
        # vals = {
        #     'top4': top4
        # }
        # response = http.Response(template='hospital_snippet.top4_doctors_snippet', qcontext=vals)
        # return response.render()

        top4 = request.env['hr.employee'].search_read([('is_doctor', '=', True)],
                                                      ['name', 'image_1920'], order='op_count desc')
        return top4

    @http.route(['/doctor/<model("hr.employee"):doctor>'], type='http', auth='public', website=True)
    def doctor_template(self, doctor):
        vals = {
            'doctor': doctor
        }
        return request.render('hospital_snippet.doctor_template', vals)

