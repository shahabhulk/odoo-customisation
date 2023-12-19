{
    'name': 'Task purchase security',
    'version': '16.0.1',
    'summary': 'purchase security',
    'category': 'secure',
    'author': '',
    'license': 'AGPL-3',
    'depends': ['purchase'],
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/purchase_secure_view.xml'
    ]
}