{
    'name': "Real Estate",
    'version': '18.0.1.1',
    'depends': ['base', 'sale_management'],
    'author': "Cybrosys",
    'category': "Business",
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tags.xml',
        'views/estate_property_offers.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True
}
