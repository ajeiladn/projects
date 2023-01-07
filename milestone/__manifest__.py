{
    'name': 'Milestone',
    'version': '16.0.1.0.0',
    'sequence': '-30',
    'summary': 'milestone',

    'depends': [
        'sale',
        'project',
    ],

    'data': [
        'views/sale_order_line.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}