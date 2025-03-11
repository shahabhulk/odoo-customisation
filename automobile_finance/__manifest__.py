{
    'name': 'Automobile Finance',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Finance Module for Automobiles',
    'author': 'Your Name',
    'depends': ['base','mail','portal','website'],
    'data': [
        'security\ir.model.access.csv',
        'data/data.xml',
        'views/finance_income_view.xml',
        'views/finance_expense_view.xml',
        'views/finance_report.xml'
    ],
    'installable': True,
    'application': True,
}
