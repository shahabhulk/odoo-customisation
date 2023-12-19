# manifest.py

{
    'name': 'task material transfer',
    'version': '16.0.1.0.0',  # Change the version as needed
    'summary': 'material transfer',
    'category': 'work',
    'author': 'Your Name',
    'license': 'AGPL-3',
    'depends': ["stock","product"],  # List of dependencies
    'installable': True,
    'data':[
        "views/menu.xml",
        "views/material_list.xml"

    ]

}
