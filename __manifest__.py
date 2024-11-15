# asset_depreciation/__manifest__.py
{
    'name': 'Asset Depreciation Management',
    'version': '1.0',
    'summary': 'Manage asset depreciation with advanced ORM techniques',
    'category': 'Accounting',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_views.xml',
        'data/asset_data.xml',
    ],
    'installable': True,
    'application': True,
}
