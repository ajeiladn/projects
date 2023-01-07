from odoo import fields, models, api
from odoo.tools import date_utils
import io
import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class PatientReportWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = 'patient report wizard'

    patient_id = fields.Many2one("res.partner", string='Patient', domain=[('is_op_created', '=', True)])
    doctor_id = fields.Many2one('hr.employee', string='Doctor')
    dept_id = fields.Many2one(string='Department', related='doctor_id.department_id')
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    disease_id = fields.Many2one('hospital.management.disease', string='Disease')

    # @api.onchange('patient_id')
    # def onchange_patient_id(self):
    #     doctors = self.env['hospital.management.op'].search([('patient_id', '=', self.patient_id.id)])
    #     return {'domain': {'doctor_id': [('id', 'in', doctors.doctor_id.ids)]}}

    def action_pdf(self):
        query = """
                SELECT
                hospital_management.patient_sequence,
                hospital_management_op.token_no,
                res_partner.name as patient,
                hospital_management_consultation.date,
                hr_employee.name as doctor,
                hr_department.name as dept,
                hospital_management_disease.disease
                
                FROM hospital_management_consultation
                INNER JOIN hospital_management on hospital_management.id=hospital_management_consultation.card_id
                INNER JOIN res_partner on hospital_management.patient_id=res_partner.id
                INNER JOIN hr_employee on hospital_management_consultation.doctor_id=hr_employee.id
                INNER JOIN hospital_management_disease on hospital_management_disease.id=hospital_management_consultation.disease_id
                INNER JOIN hr_department on hr_department.id=hospital_management_consultation.department_id
                INNER JOIN hospital_management_op on hospital_management_op.id=hospital_management_consultation.token_no
                """
        if self.patient_id:
            query += """ WHERE res_partner.name='%s' """ % self.patient_id.name
        if self.doctor_id:
            query += """ AND hr_employee.name='%s' """ % self.doctor_id.name
        if self.dept_id:
            query += """ AND hr_department.name='%s' """ % self.dept_id.name
        if self.disease_id:
            query += """ AND hospital_management_disease.disease='%s' """ % self.disease_id.disease
        if self.from_date:
            query += """ AND hospital_management_consultation.date>='%s' """ % self.from_date
        if self.to_date:
            query += """ AND hospital_management_consultation.date<='%s' """ % self.to_date

        self.env.cr.execute(query)
        vals = self.env.cr.dictfetchall()

        data = {
            'patient_id': self.patient_id.name,
            'doctor_id': self.doctor_id.name,
            'dept': self.dept_id.name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'disease': self.disease_id.disease,
            'vals': vals,
        }
        return self.env.ref('hospital_management.report_patient_report').report_action(None, data=data)

    def action_excel(self):
        query = """
                SELECT
                hospital_management.patient_sequence,
                hospital_management_op.token_no,
                res_partner.name as patient,
                hospital_management_consultation.date,
                hr_employee.name as doctor,
                hr_department.name as dept,
                hospital_management_disease.disease

                FROM hospital_management_consultation
                INNER JOIN hospital_management on hospital_management.id=hospital_management_consultation.card_id
                INNER JOIN res_partner on hospital_management.patient_id=res_partner.id
                INNER JOIN hr_employee on hospital_management_consultation.doctor_id=hr_employee.id
                INNER JOIN hospital_management_disease on hospital_management_disease.id=hospital_management_consultation.disease_id
                INNER JOIN hr_department on hr_department.id=hospital_management_consultation.department_id
                INNER JOIN hospital_management_op on hospital_management_op.id=hospital_management_consultation.token_no
                """
        if self.patient_id:
            query += """ WHERE res_partner.name='%s' """ % self.patient_id.name
        if self.doctor_id:
            query += """ AND hr_employee.name='%s' """ % self.doctor_id.name
        if self.dept_id:
            query += """ AND hr_department.name='%s' """ % self.dept_id.name
        if self.disease_id:
            query += """ AND hospital_management_disease.disease='%s' """ % self.disease_id.disease
        if self.from_date:
            query += """ AND hospital_management_consultation.date>='%s' """ % self.from_date
        if self.to_date:
            query += """ AND hospital_management_consultation.date<='%s' """ % self.to_date

        self.env.cr.execute(query)
        vals = self.env.cr.dictfetchall()

        data = {
            'patient_id': self.patient_id.name,
            'doctor_id': self.doctor_id.name,
            'dept': self.dept_id.name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'disease': self.disease_id.disease,
            'vals': vals,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'patient.report.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        patient_id = data['patient_id']
        doctor_id = data['doctor_id']
        from_date = data['from_date']
        to_date = data['to_date']

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px', 'color': '#1b5994', 'border': 1})
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        table_head = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'color': '#1b5994'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})

        sheet.merge_range('G3:R4', 'MEDICAL REPORT', head)
        if doctor_id:
            sheet.merge_range('I7:J7', 'Doctor:', cell_format)
            sheet.merge_range('K7:L7', doctor_id, txt)
        if from_date:
            sheet.merge_range('I8:J8', 'From:', cell_format)
            sheet.merge_range('K8:L8', from_date, txt)
        if to_date:
            sheet.merge_range('M8:N8', 'To:', cell_format)
            sheet.merge_range('O8:P8', to_date, txt)

        sheet.write('G10', 'SL', table_head)
        sheet.write('H10', 'OP', table_head)
        sheet.merge_range('I10:J10', 'Patient Name', table_head)
        sheet.merge_range('K10:L10', 'Date', table_head)
        sheet.merge_range('M10:N10', 'Doctor', table_head)
        sheet.merge_range('O10:P10', 'Department', table_head)
        sheet.merge_range('Q10:R10', 'Disease', table_head)

        index = 1
        col = 6
        row = 10
        for val in data['vals']:
            sheet.write(row, col, index, txt)
            sheet.write(row, col+1, val['token_no'], txt)
            sheet.merge_range(row, col+2, row, col+3, val['patient'], txt)
            sheet.merge_range(row, col+4, row, col+5, val['date'], txt)
            sheet.merge_range(row, col+6, row, col+7, val['doctor'], txt)
            sheet.merge_range(row, col+8, row, col+9, val['dept'], txt)
            sheet.merge_range(row, col+10, row, col+11, val['disease'], txt)
            if patient_id:
                sheet.merge_range('K5:N5', str(val['patient_sequence'])+str(patient_id), cell_format)
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
