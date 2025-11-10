{
    'name': 'Employee Components Request',
    'depends': ['base','hr','sale_management','purchase','stock'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/components_security_groups.xml',
        'security/ir.model.access.csv',
        'data/component_warehouse_location.xml',
        'views/components_request_view.xml',
    ]
}
