from odoo import http
from odoo.http import request


class AppointmentForm(http.Controller):
    @http.route(['/appointment/tree'], type='http', auth='public', website=True, csrf=False)
    def appointment_tree(self):
        appointments = request.env['hospital.management.appointment'].sudo().search([('is_backend', '=', False)])
        return request.render('hospital_management.appointment_tree_template', {'appointments': appointments})

    @http.route(['/appointment/form'], type='http', auth='public', website=True, csrf=False)
    def appointment_form(self):
        patient_details = request.env['hospital.management'].sudo().search([])
        doctor_details = request.env['hr.employee'].sudo().search([('is_doctor', '=', True)])
        return request.render('hospital_management.appointment_form_template', {'patient_details': patient_details,
                                                                                'doctor_details': doctor_details})

    @http.route(['/appointment/form/submit'], type='http', auth='public', website=True, csrf=False)
    def appointment_submit(self, **post):
        request.env['hospital.management.appointment'].sudo().create({
            'card_id': post.get('patient'),
            'doctor_id': post.get('doctor'),
            'date': post.get('date'),
            'is_backend': False
        })
        return request.render('hospital_management.appointment_submit')

    @http.route(['/patient-card/form'], type='http', auth='public', website=True, csrf=False)
    def create_card(self):
        patients = request.env['res.partner'].sudo().search([('is_op_created', '=', False)])
        return request.render('hospital_management.patient_card_form_template', {'patients': patients})

    @http.route(['/patient-card/form/create'], type='http', auth='public', website=True, csrf=False)
    def patient_card_create(self, **post):
        card = request.env['hospital.management'].sudo().create({
            'patient_id': post.get('patient'),
            'blood_group': post.get('blood_group')
        })
        patient_details = request.env['hospital.management'].sudo().search([])
        doctor_details = request.env['hr.employee'].sudo().search([('is_doctor', '=', True)])
        return request.render('hospital_management.appointment_form_template', {"card": card,
                                                                                'patient_details': patient_details,
                                                                                'doctor_details': doctor_details})
