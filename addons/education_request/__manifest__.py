{
    'name': 'Pengajuan Pendidikan dan Pelatihan',
    'version': '1.0',
    'summary': 'Formulir pengajuan peserta pendidikan dan pelatihan',
    'category': 'Human Resources',
    'author': 'Internal',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/education_request_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}