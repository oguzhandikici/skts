from odoo import fields, models


class PaymentPlan(models.TransientModel):
    _name = 'skts.payment.plan.wizard'
    _description = "Payment Plan Wizard"

    registration_ids = fields.Many2many('skts.registration')

    term_ids = fields.Many2many('skts.place.term', string="Terms")
    # domain_term_ids = fields.One2many('skts.place.term', store=False)

    price = fields.Integer(required=True, string="Price (₺)")

    def create_payment_plan(self):
        vals_list = []
        for registration_id in self.registration_ids:
            registration_term_ids = registration_id.place_term_ids

            for term_id in self.term_ids:
                if term_id in registration_term_ids:
                    term_payment_plan_ids = term_id.payment_plan_ids
                    registration_payment_plan_ids = registration_id.payment_ids.mapped('payment_plan_id')

                    for term_payment_plan_id in term_payment_plan_ids:
                        if term_payment_plan_id not in registration_payment_plan_ids:

                            value = {
                                'registration_id': registration_id.id,
                                'payment_plan_id': term_payment_plan_id.id,
                                'name': term_payment_plan_id.name,
                                'price': self.price,
                                'expected_date': term_payment_plan_id.expected_date,
                                'sequence': term_payment_plan_id.sequence,
                                'term_id': term_id.id,
                            }
                            vals_list.append(value)
        if vals_list:
            self.env['skts.payment'].create(vals_list)
