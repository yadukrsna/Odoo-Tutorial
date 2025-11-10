{
    'name': 'Test Website',
    'depends': ['base', 'sale_management', 'website', 'website_sale'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'data': [
        'view/add_cart_template.xml',
        'view/custom_product.xml'
    ]
}
