{
    'name': 'Hospital Management',
    'version': '16.0.1.0.0',
    'sequence': '-32',
    'summary': 'hospital_management',

    'depends': [
        'contacts',
        'account',
        'hr',
        'website',
    ],

    'data': [
        'security/hospital_management_security.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',

        'data/hospital_management_sequence.xml',
        'data/hospital_management_sequence_op.xml',
        'data/hospital_management_sequence_appointment.xml',
        'data/job_position_demo.xml',
        'data/product_demo.xml',

        'wizard/patient_report_wizard.xml',

        'report/ir_actions_reports.xml',
        'report/ir_actions_templates.xml',

        'views/hospital_management.xml',
        'views/res_partner_views.xml',
        'views/hospital_management_op.xml',
        'views/hospital_management_consultation.xml',
        'views/hospital_management_disease.xml',
        'views/hr_employee.xml',
        'views/hospital_management_medicine.xml',
        'views/hospital_management_appointment.xml',

        'views/website_appointment_templates.xml',
        'views/website_menus.xml',

        'views/hospital_management_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'hospital_management/static/src/js/patient_report.js',
        ],
        'web.assets_frontend': [
            'hospital_management/static/src/js/appointment_form.js',
        ],
    }
}
