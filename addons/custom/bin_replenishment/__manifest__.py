# Bin Replenishment Module
{
    'name': 'Bin Replenishment',
    'version': '14.0.0',
    'summary': 'Bin Replenishment Automation',
    'category': 'Inventory',
    'author': 'Dipu Sharma',
    'maintainer': 's',
    'company': '',
    'website': '',
    'depends': [
        'base',
        'stock',
        'l10n_latam_invoice_document',
        'l10n_latam_base',
        ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/add_name.xml',
        'views/bin_replenishment_view.xml',
        'data/bin_replenishment_data.xml'
    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
