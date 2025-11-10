{
    'name': "POS Stock Location",
    'version': '1.0',
    'depends': ['base', 'point_of_sale', 'stock', 'contacts'],
    'license': 'LGPL-3',
    'data': [
        'views/res_config_settings_view.xml',
        'views/res_partner_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_extension/static/src/js/pos_avail_qty.js',
            'pos_extension/static/src/js/pos_credit_limit.js',
            'pos_extension/static/src/xml/pos_avail_qty.xml',
            'pos_extension/static/src/overrides/components/custom_popup.js',
            'pos_extension/static/src/overrides/components/custom_popup.xml',
            'pos_extension/static/src/js/pos_discount.js',
            'pos_extension/static/src/xml/pos_discount.xml'
        ],
    },
}
