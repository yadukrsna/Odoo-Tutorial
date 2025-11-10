{
    'name': 'Product Threshold',
    'depends': ['base', 'sale_management', 'contacts'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'data': [
        'views/res_partner_view.xml',
        'views/res_config_settings_view.xml',
    ]
}