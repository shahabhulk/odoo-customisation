{
    'name': 'Weather App',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Fetches weather updates for cities',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/weather.xml',
    ],
    'installable': True,
    'application': True,
}
