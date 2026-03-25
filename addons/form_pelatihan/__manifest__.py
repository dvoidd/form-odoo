{
    'name': 'Form Pelatihan',
    'version': '1.0.0',
    'summary': 'Modul Pengajuan Pendidikan & Pelatihan',
    'author': 'Custom',
    'depends': ['base', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/master_data_views.xml',
        'views/form_pelatihan_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}