{
    'name': 'Proposal Pengajuan Training',
    'version': '1.0',
    'summary': 'Modul untuk mengelola proposal In-House Training ToT',
    'category': 'Human Resources',
    'author': 'Internal',
    'depends': ['base', 'education_request'],
    'data': [
        'security/ir.model.access.csv',
        'views/proposal_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}