# -*- coding: utf-8 -*-
{
    'name': 'Sap Integration',
    'version': '16.0.1.0.0',
    'summary': 'Odoo Sap Integration',
    'description': """
        Odoo Sap Integration
    """,
    'depends': ['base', 'sale', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sap_integration.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
