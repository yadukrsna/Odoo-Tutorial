{
    'name': "Last Sales Date",
    'version': '1.0',
    'depends': ['base', 'contacts', 'account', 'sale_management', 'purchase'],
    'license': 'LGPL-3',
    'data': [
        'data/default_rounding_product.xml',
        'views/res_partner_views.xml'
    ],
    'installable': True,
    'application': False,
}
