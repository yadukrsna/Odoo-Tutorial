{
    'name': 'Associated Products',
    'depends': ['base', 'sale', 'contacts'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/product_template_view.xml',
    ]
}
