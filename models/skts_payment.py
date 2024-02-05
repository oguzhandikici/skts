from odoo import models, fields, api, _


class Payment(models.Model):
    _name = "skts.payment"
    _description = "Payments"
    _order = "expected_date asc"
    _rec_name = "name"

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

    # sequence = fields.Integer(default=1, string="Payment Order")
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
    ], default='early')

    @api.depends("date")
    def _compute_color(self):
        for record in self:
            if record.date:
                record.color = 10
            else:
                record.color = 2

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.registration_id.compute_payment_status()
        return res

    def write(self, vals):
        if 'date' in vals:
            if vals['date'] is False:
                vals['type'] = False

        res = super(Payment, self).write(vals)

        compute_status = any(edited_field in ['expected_date', 'date'] for edited_field in vals)
        if compute_status:
            self.mapped('registration_id').compute_payment_status()
        return res


class PlaceTermPayment(models.Model):
    _name = "skts.place.term.payment.plan"
    _description = "Place Term Payment Plan"
    _order = "expected_date asc"

    term_id = fields.Many2one('skts.place.term')
    name = fields.Char(required=True)
    expected_date = fields.Date()

    sequence = fields.Integer(default=1, string="Payment Order")
