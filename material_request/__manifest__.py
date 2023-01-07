{
    'name': 'Material Request',
    'version': '16.0.1.0.0',
    'sequence': '-27',
    'summary': 'material_request',

    'depends': [
        'contacts',
        'stock',
        'purchase',
    ],

    'data': [
        'security/material_request_security.xml',
        'security/ir.model.access.csv',

        'data/material_request_sequence.xml',

        'views/material_request.xml',
        'views/material_request_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}