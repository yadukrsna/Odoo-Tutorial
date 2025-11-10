from odoo import fields, models, _


class TransferWizard(models.TransientModel):
    _name = 'employee.transfer.wizard'
    _description = 'Employee Transfer Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    transfer_company_id = fields.Many2one('res.company', 'Requested Transfer Company', required=True)

    def action_confirm_transfer(self):
        self.ensure_one()

        self.employee_id.write({
            'transfer_company_id': self.transfer_company_id.id
        })

        admin_user = self.env.ref('base.user_admin', raise_if_not_found=False)

        message = _("Transfer Request: %s has requested transfer to company %s.") % (
            self.employee_id.name, self.transfer_company_id.name
        )

        if admin_user:
            general_channel = self.env['discuss.channel'].search([
                ('name', '=', 'general')
            ], limit=1)

            if general_channel:
                general_channel.message_post(
                    body=message,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                )
        return {'type': 'ir.actions.act_window_close'}
