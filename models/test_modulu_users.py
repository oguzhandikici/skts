from odoo import models, fields, api


class TestModuluUsers(models.Model):
    _name = "test_modulu.users"
    _description = "Keeps user and password information"

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id,
                              readonly=lambda self: False if self.user.has_group('test_addon.group_test_modulu_manager') else True)
    reveal_pw = fields.Boolean(store=False, string='Reveal Password')

    name = fields.Char()
    password = fields.Char()
    revealed_pw = fields.Char(related='password')

    @api.onchange('reveal_pw')
    def reveal_password(self):
        if self.reveal_password:
            self.env['test_modulu.log'].create({
                'accessor_user_id': self.env.user.id,
                'access_date': fields.datetime.now(),
                'accessed_password_id': self.id,
            })
