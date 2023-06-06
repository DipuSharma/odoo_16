# sg_sku_calculator module creation
{
    'name': 'Restaurant',
    'version': '15.0.1.0.0',
    'summary': 'Restaurant',
    'category': 'Inventory',
    'author': 'Restaurant',
    'maintainer': 'Sku-Calculator',
    'company': 'DreamzTech Solutions',
    'website': 'https://www.dreamztech.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/restaurant_views.xml',
        'views/menu_views.xml',
        'reports/staff_report.xml'
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'sg_sku_calculator/static/src/js/sku_calculator.js',
    #     ]},
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
