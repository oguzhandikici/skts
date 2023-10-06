from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Payment(models.Model):
    _name = "skts.payment"
    _description = "Payments"
    _order = "sequence"
    _rec_name = "display_name"

    display_name = fields.Html(compute="_compute_display_name")
    name = fields.Char(string="Payment Name", required=True)
    price = fields.Integer(required=True, string="Price (₺)")
    date = fields.Date(string="Payment Date")
    type = fields.Selection([
        ('iban', 'IBAN'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ], string="Payment Type")

    sequence = fields.Integer(default=1, string="Payment Order")
    color = fields.Integer('Color Index', compute="_compute_color")

    registration_id = fields.Many2one("skts.registration", required=True, ondelete="cascade")

    @api.depends("date")
    def _compute_color(self):
        for record in self:
            if record.date:
                record.color = 10
            else:
                record.color = 2

    @api.depends("name", "price")
    def _compute_display_name(self):
        green_flag = False
        for record in self:
            if record.id:
                if record.date:
                    is_paid = '/ <font color="green">Ödendi</font>'
                elif not green_flag:
                    is_paid = '/ <font color="orange">Bekliyor</font>'
                    green_flag = True
                elif green_flag:
                    is_paid = '/ <font color="gray">Bekliyor</font>'

                record.display_name = f"<b>{record.name} / ₺{record.price} {is_paid}</b>"

            else:
                record.display_name = '<b><font color="pink">Kaydet tuşuna basın</font></b>'

    @api.model_create_multi
    def create(self, vals_list):
        for value in vals_list:
            new_sequence = len(self.env['skts.registration'].browse([value['registration_id']]).payment_ids) + 1
            value['sequence'] = new_sequence
        return super().create(vals_list)
