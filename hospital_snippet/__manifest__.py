{
    'name': 'Hospital Snippet',
    'version': '16.0.1.0.0',
    'sequence': '-100',
    'summary': 'hospital_snippet',

    'depends': [
        'base',
        'hospital_management',
        'website',
    ],

    'data': [
        'views/doctor_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'hospital_snippet/static/src/js/doctor_snippet.js',
            'hospital_snippet/static/src/xml/qweb_doctor_carousal.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,

}
