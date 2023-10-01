from odoo import models, fields, api


class SKTSDriver(models.Model):
    _name = "skts.driver"
    _description = "Drivers"

    name = fields.Char(required=True)
    user_id = fields.Many2one("res.users")
    number = fields.Integer()
    seats = fields.Integer(required=True)

    can_see_driver_numbers = fields.Char(default="[]", help="ex: [244,231]")
    iban = fields.Text()

    morning_registration_ids = fields.One2many("skts.registration", "morning_driver_id")
    evening_registration_ids = fields.One2many("skts.registration", "evening_driver_id")
