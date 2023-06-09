# sg_sku_calculator module creation
{
    'name': 'Barcode Report View',
    'version': '15.0.1.0.0',
    'summary': 'Extended Barcode Report View',
    'category': 'Inventory',
    'author': 'Dipu Sharma',
    'maintainer': 'Dipu Sharma',
    'company': '',
    'website': '',
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
        'stock',
        'sale',
        'purchase',
    ],
    'data': [
        'reports/barcode_extend_report.xml',
        'views/api_key_add.xml'
    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
