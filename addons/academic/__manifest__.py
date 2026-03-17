{
    'name': 'Academic Management',
    'version': '1.0',
    'summary': 'Modul untuk mengelola Course dan Session',
    'category': 'Education',
    'author': 'Internal',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/academic_views.xml',
        'views/session.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}