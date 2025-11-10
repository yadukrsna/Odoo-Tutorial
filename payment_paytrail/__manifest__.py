{
    'name': 'Paytrail Payment Integration',
    'category': 'Accounting/Payment',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['payment'],
    'data': [
        'views/payment_paytrail_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
