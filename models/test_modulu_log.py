from odoo import models, fields, api


class SktsOkul(models.Model):
    _name = "test_modulu.log"
    _description = "Keeps access logs of 'test_modulu.users' model"

    accessor_user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    access_date = fields.Datetime(default=fields.Datetime.now)

    accessed_password_id = fields.Many2one("test_modulu.users")
