# manifest.py

{
    'name': 'task pos product owner',
    'version': '16.0.0.0',  # Change the version as needed
    'summary': 'pos product owner',
    'category': 'work',
    'author': 'Your Name',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'product'],  # List of dependencies
    'installable': True,
    'data': [
        'views/product_owner.xml',
    ],
    'assets': {
        'point_of_sale.assets': [

            'task_pos_product_owner/static/src/xml/pos_screen.xml',
        ],
    },

}
