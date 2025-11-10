{
    'name': "POS Product Screen",
    'version': '1.0',
    'depends': ['sale_management', 'point_of_sale'],
    'license': 'LGPL-3',
    'data': [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_screen/static/src/js/custom_product_button.js',
            'pos_product_screen/static/src/js/custom_product_screen.js',
            'pos_product_screen/static/src/xml/custom_product_button.xml',
            'pos_product_screen/static/src/xml/custom_product_screen.xml',
        ],
    },
    'installable': True,
    'application': False,
}
