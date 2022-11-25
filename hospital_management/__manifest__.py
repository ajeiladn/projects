{
    'name': 'Hospital Management',
    'version': '16.0.1.0.0',
    'sequence': '-25',
    'summary': 'hospital_management',

    'depends': [

    ],

    'data': [
        'security/ir.model.access.csv',
        'views/hospital_management.xml',
        'views/res_partner_views.xml',
        'data/hospital_management_sequence.xml',
        'view/hospital_management_op.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}