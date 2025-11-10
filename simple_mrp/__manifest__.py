{
    'name': 'Simple MRP',
    'depends': ['base', 'stock', 'mrp', 'purchase'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_simple_mo.xml',
        'views/simple_mo_view.xml',
        'views/simple_bom_view.xml',
    ]
}