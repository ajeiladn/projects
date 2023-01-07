{
    'name': 'Multiple Invoice',
    'version': '16.0.1.0.0',
    'sequence': '-32',
    'summary': 'invoice for multiple sale order',

    'depends': [
        'sale',
        'account',
    ],

    'data': [
        'views/account_move.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}