from odoo import models, fields, api


class SKTSDriver(models.Model):
    _name = "skts.driver"
    _description = "Drivers"

    name = fields.Char(required=True)
    user_id = fields.Many2one("res.users")
    number = fields.Integer()

    can_see_driver_numbers = fields.Char(default="[]", help="ex: [244,231]")
    iban = fields.Text()
