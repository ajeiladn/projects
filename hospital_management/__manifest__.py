{
    'name': 'Hospital Management',
    'version': '16.0.1.0.0',
    'sequence': '-25',
    'summary': 'hospital_management',

    'depends': [
        'contacts',
        'hr',
    ],

    'data': [
        'security/ir.model.access.csv',

        'data/hospital_management_sequence.xml',
        'data/hospital_management_token.xml',

        'views/hospital_management.xml',
        'views/res_partner_views.xml',
        'views/hospital_management_op.xml',
        'views/hospital_management_consultation.xml',
        'views/hospital_management_disease.xml',
        'views/hr_employee.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}