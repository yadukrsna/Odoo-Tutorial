{
    'name': "Tolerance",
    'version': '1.0',
    'depends': ['base', 'sale_management', 'contacts', 'purchase', 'stock'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_line_views.xml',
        'views/purchase_order_line_views.xml',
        'views/stock_move_views.xml',
        'wizard/tolerance_warning.xml',
    ],
    'installable': True,
    'application': False,
}
