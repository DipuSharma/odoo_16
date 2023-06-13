# sg_sku_calculator module creation
{
    'name': 'Sku Calculator',
    'version': '14.0.0',
    'summary': 'Generates Sku using Sku Calculator with Product categories, type and etc.',
    'description': """
        Sku Calculator for use sku code of product using product category, product type etc.
    """,
    'summary': 'Generates SKU with the help of SKU Calculator',
    'category': 'Inventory',
    'author': 'Sku-Calculator',
    'maintainer': 'Sku-Calculator',
    'company': '',
    'website': '',
    'depends': ['web', 'base' 'product'],
    'data': [
        # Assets
        # 'views/assets.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/sku_page_pt_views.xml',
        'views/sku_categories.xml',
        'views/sku_volumes.xml',
        'views/sku_vendor.xml',
        'views/sku_shape_color.xml',
        'views/sku_bonded.xml',
        'views/sku_country.xml',
        'views/sku_product_type.xml',
        'data/sku_categories_data.xml',
        'data/sku_types_data.xml',
        'data/sku_shapes_data.xml',
        'data/sku_countries_data.xml',
        'data/sku_bonded_data.xml',
        'data/sku_volumes_data.xml',
        'data/sku_vendors_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'sg_sku_calculator/static/src/js/calculator.js',
            # 'sg_sku_calculator/static/src/js/test.js',
        ]},
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
