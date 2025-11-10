from datetime import date, timedelta
from odoo import fields, models, api, Command
from odoo.exceptions import UserError


class HotelManagementAccommodation(models.Model):
    """This model is used for ACCOMMODATION of guests accordingly"""
    _name = 'hotel.management.accommodation'
    _description = 'Hotel Management Accommodation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(readonly=True, default="New", string="Sequence")
    guest_id = fields.Many2one("res.partner", string="Guest Name", required=True)
    guest_number = fields.Integer("Guest Number", default=1)
    other_guest_ids = fields.One2many("hotel.management.guest", 'hotel_id',
                                      string="Other Guest")
    check_in = fields.Datetime("Check In", default=lambda self: fields.datetime.now())
    check_out = fields.Datetime("Check Out")
    bed_type = fields.Selection(related="room_id.bed", store=True, readonly=False)
    facility_id = fields.Many2many("hotel.management.facility", string="Facilities",
                                   readonly=False)
    room_id = fields.Many2one("hotel.management.room", "Rooms", readonly=False)
    state = fields.Selection(
        [('draft', 'Draft'), ('check in', 'Check In'), ('check out', 'Check Out'), ('cancel', 'Cancel')],
        default='draft')
    id_proof = fields.Boolean("Identification Proof", default=False)
    id_number = fields.Binary("Id Proof", attachment=True)
    expected_days = fields.Integer("Expected Days")
    expected_date = fields.Datetime("Expected Check Out", compute="_compute_expected_date", store=True)
    room_domain = fields.Binary(compute='_compute_bed_type')
    order_list_ids = fields.One2many('hotel.management.order.list', 'order_id')
    order_food_ids = fields.One2many('hotel.management.order.food', 'accommodation_id')
    invoice_id = fields.Many2one("account.move")
    payment_ids = fields.One2many('hotel.management.payment', 'accommodation_id')
    payment_status = fields.Selection(related="invoice_id.payment_state")
    total_amount = fields.Monetary('Total Amount', compute='_compute_total', currency_field='currency_id', store=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.ref('base.USD'))
    count = fields.Integer(compute='_compute_count')
    date_expected = fields.Date(compute="_compute_date_expected", store=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    cancelled_date = fields.Date('Canceled Date', store=True)
    active = fields.Boolean('is_active', default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)
    website_id = fields.Many2one('website', 'Website')

    def create(self, vals):
        """This function is used to set a unique sequence for each accommodation"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.management.accommodation') or 'New'
        return super(HotelManagementAccommodation, self).create(vals)

    @api.depends('bed_type', 'facility_id')
    def _compute_bed_type(self):
        for record in self:
            record.room_domain = [('state', '=', 'available')]
            if record.bed_type:
                record.room_domain.append(('bed', 'in', [record.bed_type]))
            if record.facility_id:
                record.room_domain.append(('facility_ids', '=', record.facility_id.ids))

    @api.depends("check_in", "expected_days")
    def _compute_expected_date(self):
        """Calculation of the Expected number of days the guest proposes to stay"""
        for record in self:
            check_in_dt = fields.Datetime.to_datetime(record.check_in)
            record.expected_date = check_in_dt + timedelta(days=record.expected_days)
    @api.depends('payment_ids.subtotal')
    def _compute_total(self):
        """Function to compute the total amount"""
        for record in self:
            record.total_amount = sum(record.subtotal for record in record.payment_ids)

    @api.depends('order_food_ids')
    def _compute_count(self):
        """Function to compute the count of orders generated"""
        for record in self:
            record.count = len(record.order_food_ids)

    @api.depends("expected_date")
    def _compute_date_expected(self):
        for record in self:
            record.date_expected = record.expected_date.date() if record.expected_date else False

    def action_cancel(self):
        self.write({'state': 'cancel', 'cancelled_date': date.today()})

    def check_in_action(self):
        """Check In button action.Actions that occurs when the guest tries to check in"""
        hotel_rent_product = self.env.ref('hotel_management.default_hotel_management_product_rent')
        for record in self:
            record.room_id.state =  'not available'
            record.write({'state': 'check in',
                          'check_in': fields.datetime.now(),
                          'payment_ids': [Command.create({
                              'product_id': hotel_rent_product.id,
                              'unit_price': record.room_id.rent,
                              'quantity': 1,
                              'uom_id': record.room_id.uom_id.id,
                              'subtotal': record.room_id.rent
                          })]
            })
            if len(record.other_guest_ids) > record.guest_number - 1:
                raise UserError(f"You can only add {record.guest_number} guests.")
            if len(record.other_guest_ids) < record.guest_number - 1:
                raise UserError("Please provide all guest details.")
            if not self.env['ir.attachment'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id)
            ]):
                raise UserError("Please attach a file.")

    def check_out_action(self):
        """Check Out button action.Actions that occurs when the guest tries to check out"""
        for record in self:
            record.room_id.state = 'available'
            record.write({'state': 'check out', 'check_out': fields.datetime.now()})
            hotel_rent_product = self.env.ref('hotel_management.default_hotel_management_product_rent')
            restaurant_cost_product = self.env.ref('hotel_management.default_hotel_management_product_restaurant')

            invoice_lines = [(0, 0, {
                'product_id': restaurant_cost_product.id,
                'quantity': 1,
                'price_unit': line.total_amount})
                             for line in record.order_food_ids]

            invoice_lines.append((0, 0, {
                'product_id': hotel_rent_product.id,
                'quantity': 1,
                'price_unit': self.room_id.rent
            }))

            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.guest_id.id,
                'invoice_origin': self.name,
                'invoice_line_ids': invoice_lines,
                'invoice_date': fields.Date.today(),
            })
            record.invoice_id = invoice.id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_view_invoice(self):
        """Action to view the Invoice generated"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('id', 'in', self.invoice_id.ids)],
            'target': 'current'
        }

    def action_order_food(self):
        """Action To Order Food"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Order Food',
            'view_mode': 'list,form',
            'res_model': 'hotel.management.order.food',
            'domain': [('id', 'in', self.order_food_ids.ids)],
            'context': {
                'default_accommodation_id': self.id,
                'default_name': self.room_id.id,
                'default_guest_id': self.guest_id.id
            },
            'target': 'current'
        }

    @api.model
    def accommodation_days(self):
        """Function for schedule action to increment quantity and archive cancelled accommodation"""
        today = date.today()
        for record in self.search([('state', '=', 'check in')]):
            if record.payment_ids:
                record.payment_ids.quantity += 1
            if record.date_expected == today:
                self.env.ref('hotel_management.email_template_hotel').send_mail(record.id, force_send=True)

        self.search([('state', '=', 'cancel'),
                     ('cancelled_date', '<=', date.today() - timedelta(days=2))]).write({'active': False})

    def unlink(self):
        for record in self:
            if record.room_id:
                record.room_id.state = 'available'

        return super().unlink()
