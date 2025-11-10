{
    'name': 'Employee Transfer',
    'depends': ['hr'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_user_view.xml',
        # 'wizard/employee_transfer_wizard_view.xml',
        'views/hr_employee_view.xml',
    ]
}
