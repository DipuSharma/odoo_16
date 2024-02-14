{
    'name': 'Restaurant',
    'version': '15.0.1.0',
    'summary': 'Restaurant',
    'description': """To manage restaurant""",
    'category': 'Inventory',
    'author': 'Restaurant',
    'maintainer': 'Sku-Calculator',
    'company': '',
    'website': '',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/restaurant_views.xml',
        'views/res_partner.xml',
        'views/menu_views.xml',
        'reports/staff_report.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'restaurant/static/src/js/restaurant.js',
            'restaurant/static/src/components/*/*.js',
        ],
        'web.assets_qweb': [
        	  'website_product_publish/static/src/xml/restaurant_widget.xml',
    	],},
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
