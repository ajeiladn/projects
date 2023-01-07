{
    'name': 'Automated Purchase Order',
    'version': '16.0.1.0.0',
    'sequence': '-29',
    'summary': 'automatic purchase order',

    'depends': [
        'stock',
        'purchase',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'wizard/product_template_wizard.xml',
        # 'views/purchase_order.xml',
    ],

    'demo': [],
    'css': [],

    'installable': True,
    'application': True,
    'auto_install': False,
}
