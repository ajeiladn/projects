{
    'name': 'Account Move Custom',
    'version': '15.0.1.0.12',
    'sequence': -101,
    'summary': "account_move_custom",
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_move_line.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}