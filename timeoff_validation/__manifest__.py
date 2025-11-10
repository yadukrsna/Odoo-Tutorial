{
    'name': 'Time Off Validation',
    'depends': ['hr_holidays'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'data': [
        'data/allocation_expiry_email.xml',
        'data/ir_cron_allocation.xml',
        ]
}
