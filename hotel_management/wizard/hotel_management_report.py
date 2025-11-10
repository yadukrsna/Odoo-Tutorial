import io
import json
import xlsxwriter
from odoo import api,fields, models
from odoo.tools.json import json_default

class HotelManagementReport(models.TransientModel):
    _name = 'hotel.management.report'
    _description = 'Hotel Management Report'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    guest_id = fields.Many2one('res.partner', 'Guest')
    room_id = fields.Many2one('hotel.management.room', 'Room No')
    room_type = fields.Selection(related='room_id.bed', readonly=False, store=True)
    room_domain = fields.Binary(compute="_compute_room")

    @api.depends('room_type')
    def _compute_room(self):
        for record in self:
            if record.room_type:
                record.room_domain = [('bed', 'in', [record.room_type])]
            else:
                record.room_domain = []

    def _get_query(self):
        query = """
                    SELECT g.name AS guest_name,
                           a.check_in AS check_in,
                           a.check_out AS check_out,
                           a.state AS state,   
                           a.bed_type AS room_type,
                           r.name AS room
                    FROM hotel_management_accommodation a
                    JOIN res_partner g ON a.guest_id = g.id
                    JOIN hotel_management_room r ON a.room_id = r.id
                    WHERE 1 = 1
                """
        param = []

        if self.guest_id:
            query += " AND g.id = %s"
            param.append(self.guest_id.id)

        if self.date_from:
            query += " AND a.check_in >= %s"
            param.append(self.date_from)

        if self.date_to:
            query += " AND a.check_out <= %s"
            param.append(self.date_to)

        if self.room_id:
            query += " AND a.room_id = %s"
            param.append(self.room_id.id)

        if self.room_type:
            query += " AND a.bed_type = %s"
            param.append(self.room_type)

        self.env.cr.execute(query, tuple(param))
        result = self.env.cr.dictfetchall()

        return result

    def action_pdf_report(self):
        data = {
            'result': self._get_query()
        }
        report_action = self.env.ref('hotel_management.action_hotel_management_report').report_action(self, data=data)
        report_action['close_on_report_download'] = True
        return report_action

    def action_xlsx_report(self):
        data = {
            'result': self._get_query()
        }

        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'hotel.management.report',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Hotel Management Excel Report',
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data ,response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size':'12px', 'align':'center', 'border': 2})
        head = workbook.add_format(
            {'align': 'center', 'bold': 'True', 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '12px', 'align': 'center', 'border':2})
        sheet.merge_range('E1:K3', 'Hotel Management Excel Report', head)

        headers = ['SL.No', 'Guest', 'Check In', 'Check Out', 'Room', 'Type', 'State']
        sheet.set_column('E:K',20)
        col = 4
        for header in headers:
            sheet.write(6, col, header, cell_format)
            col+=1

        row = 7
        sl = 1
        for record in data.get('result'):
            sheet.set_row(row, 20)
            sheet.write(row, 4, sl, txt)
            sheet.write(row, 5, record.get('guest_name', ''), txt)
            sheet.write(row, 6, record.get('check_in', ''), txt)
            sheet.write(row, 7, record.get('check_out', ''), txt)
            sheet.write(row, 8, record.get('room', ''), txt)
            sheet.write(row, 9, record.get('room_type', ''), txt)
            sheet.write(row, 10, record.get('state', ''), txt)
            sl += 1
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
