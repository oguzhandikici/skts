from odoo import http
from odoo.http import request


class RegistrationController(http.Controller):

    @http.route(['/registration/form/submit'], type='http', auth="public", website=True)
    def registration_submit(self, **post):
        print(post)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone')
        })
        vals = {
            'partner': partner,
        }
        #inherited the model to pass the values to the model from the form#
        return request.render("create_partner_by_website.tmp_customer_form_success", vals)
        #finally send a request to render the thank you page#