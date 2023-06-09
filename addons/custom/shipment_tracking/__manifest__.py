# sg_sku_calculator module creation
{
    'name': 'SG Shipment Tracking',
    'version': '15.0.1.0.0',
    'summary': 'SG Shipment Tracking',
    'category': 'Services',
    'author': '',
    'maintainer': '',
    'company': '',
    'website': '',
    'depends': [
        'web',
        'base',
        'stock',
        'product',
        'sale',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/shipment_type.xml',
        'views/shipment_view.xml',
        'views/logistic_service.xml',
        'views/purchase_order_column.xml',
        'views/menu_view.xml',
        'data/logistic_service.xml',
        'data/shipment_type.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'sg_shipment_tracking/static/src/css/my_css.css',
        ]},
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
