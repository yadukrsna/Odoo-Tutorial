{
    'name': "Customer Credit Limit",
    'version': '1.0',
    'depends': ['base', 'sale_management', 'contacts'],
    'license': 'LGPL-3',
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
'application': False,
}