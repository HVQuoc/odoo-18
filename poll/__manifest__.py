{
    'name': 'Poll module',
    'summary': 'Poll module',
    'category': 'Polling/Polling',
    'description': '''
        Poll system module
    ''',
    'sequence': 10,
    'version': '1.0',
    'license': 'LGPL-3',
    'author': 'Quoc Hoang',
    'depends': [

    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/poll_views.xml',
        'views/poll_menus.xml'
    ],
    'installable': True,
    'application': True,
}