# manifest.py

{
    'name': 'task loan management',
    'version': '16.0.1.0.0',  # Change the version as needed
    'summary': 'Loan management',
    'category': 'Loan',
    'author': 'Your Name',
    'license': 'AGPL-3',
    'depends': ['hr','sale'],  # List of dependencies
    'installable': True,
    'data':[
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/Loan.xml'
    ]

}
