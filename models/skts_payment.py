from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError


class Payment(models.Model):
    _name = "skts.payment"
    _description = "Payments"
    _order = "sequence"
    _rec_name = "name"

    display_name = fields.Html(compute="_compute_display_name")
    term_id = fields.Many2one('skts.place.term')
    name = fields.Char(string="Payment Name", required=True)
    price = fields.Integer(required=True, string="Price (₺)")
    date = fields.Date(string="Payment Date")
    type = fields.Selection([
        ('iban', 'IBAN'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ], string="Payment Type")
    expected_date = fields.Date(string='Expected Payment Date', required=True)

    sequence = fields.Integer(default=1, string="Payment Order")
    color = fields.Integer('Color Index', compute="_compute_color")

    registration_id = fields.Many2one("skts.registration", required=True, ondelete="cascade")
    registration_term_ids = fields.Many2many(related='registration_id.place_term_ids', string="Registration Terms")
    payment_plan_id = fields.Many2one('skts.place.term.payment.plan',
                                      help='Payment Plan ID if created from payment plan action', ondelete="set null")
    status = fields.Selection([
        ('paid', 'Paid'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('late', 'Late'),
        ('early', 'Early')
    ], compute='_compute_status')

    @api.depends('expected_date', 'date', 'sequence')
    def _compute_status(self):
        # TODO: BURDASIN
        records = self.sorted('sequence')
        next_payment = False
        for record in records:
            if record.expected_date:
                if record.date:
                    record.status = 'paid'
                elif not record.date and not next_payment and record.expected_date >= date.today():
                    record.status = 'awaiting_payment'
                    next_payment = True
                elif record.expected_date < date.today():
                    record.status = 'late'
                else:
                    record.status = 'early'
            else:
                record.status = ''

    @api.depends("date")
    def _compute_color(self):
        for record in self:
            if record.date:
                record.color = 10
            else:
                record.color = 2

    # @api.depends("name", "price")
    # def _compute_display_name(self):
    #     green_flag = False
    #     for record in self:
    #         if record.id:
    #             if record.date:
    #                 is_paid = '/ <font color="green">Ödendi</font>'
    #             elif not green_flag:
    #                 is_paid = '/ <font color="orange">Bekliyor</font>'
    #                 green_flag = True
    #             elif green_flag:
    #                 is_paid = '/ <font color="gray">Bekliyor</font>'
    #
    #             record.display_name = f"<b>{record.name} / ₺{record.price} {is_paid}</b>"
    #
    #         else:
    #             record.display_name = '<b><font color="pink">Kaydet tuşuna basın</font></b>'

    @api.model_create_multi
    def create(self, vals_list):
        is_wizard = self.env.context.get('wizard')
        for value in vals_list:
            if not is_wizard:
                new_sequence = len(self.env['skts.registration'].browse([value['registration_id']]).payment_ids) + 1
                value['sequence'] = new_sequence
        return super().create(vals_list)


class PlaceTermPayment(models.Model):
    _name = "skts.place.term.payment.plan"
    _description = "Place Term Payment Plan"

    term_id = fields.Many2one('skts.place.term')
    name = fields.Char(required=True)
    expected_date = fields.Date()

    sequence = fields.Integer(default=1, string="Payment Order")
