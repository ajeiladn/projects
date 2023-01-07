{
    'name': 'Sale Order Margin',
    'version': '16.0.1.0.0',
    'sequence': '-10',
    'summary': 'sale_order_margin',

    'depends': [
        "sale",
    ],

    'data': [
        'views/sale_order.xml',
        'views/sale_order_line.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}