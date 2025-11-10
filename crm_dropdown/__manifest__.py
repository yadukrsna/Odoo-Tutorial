{
    'name': "CRM Dropdown",
    'version': '1.0',
    'depends': ['crm', 'web'],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'crm_dropdown/static/src/js/crm_dropdown.js',
            'crm_dropdown/static/src/xml/crm_dropdown.xml',
        ],
    },
    'installable': True,
    'application': False,
}