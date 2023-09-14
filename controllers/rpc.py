from odoo import http
from odoo.http import request


class RegistrationWebsiteFormController(http.Controller):
    @http.route('/registration/form/domain_fields', type='json', method=['POST'], auth='public', csrf=False)
    def registration_website_form(self, **post):
        model = post.get('model')
        domain = post.get('domain')
        fields = post.get('fields')

        models_allowed = request.env["ir.config_parameter"].sudo().get_param("skts.website_form_controller_models")

        if model in models_allowed:
            demo_user = request.env.ref('base.user_demo')
            res = request.env[model].with_user(demo_user.id).search_read(domain, fields)
            return res
        else:
            return "MODEL NOT ALLOWED"
