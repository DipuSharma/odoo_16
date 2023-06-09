# Vendor grading module creation
{
    'name': 'Vendor Grading',
    'version': '14.0.0',
    'summary': 'Vendors Grading System',
    'category': 'Inventory',
    'author': 'Vendor Grading',
    'maintainer': '',
    'company': '',
    'website': '',
    'depends': ['base', 'purchase', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/vendor.grade.csv',
        'views/vendor_views.xml'
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'sg_vendor_grading/static/js/sorting_column.js',
    #     ]},
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
