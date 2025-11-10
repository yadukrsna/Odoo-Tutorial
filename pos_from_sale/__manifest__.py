{
    'name': "POS from Sales",
    'version': '1.0',
    'depends': ['sale_management', 'point_of_sale'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/pos_payment_wizard.xml'
    ],
    'installable': True,
    'application': False,
}

