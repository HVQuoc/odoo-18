{
    'name': 'Product Program Manager',
    'version': '1.0',
    'author': 'Quoc Hoang',
    'summary': 'Manage brands, products, categories and programs',
    'depends': [],
    'license': 'LGPL-3',
    'sequence': 10,
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/brand_views.xml',
        'views/product_views.xml',
        'views/category_views.xml',
        'views/program_menus.xml',
    ],
    'installable': True,
    'application': True,
}
