{
    'name': 'Sale Program Management',
    'version': '1.0',
    'author': 'Quoc Hoang',
    'summary': 'Manage brands, products, categories and programs',
    'sequence': 10,
    'license': 'LGPL-3',
    'depends': [],
    'data': [
        'data/unique_code.sequence.xml',
        'security/ir.model.access.csv',
        'views/brand_views.xml',
        'views/product_views.xml',
        'views/category_views.xml',
        'views/program_views.xml',
        'views/company_views.xml',
        'views/main_menus.xml'
    ],
    'installable': True,
    'application': True,
}
