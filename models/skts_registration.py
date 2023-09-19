from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError
import json


class RegistrationContact(models.Model):
    _name = "skts.registration.contact"
    _description = "Contacts"

    registration_id = fields.Many2one("skts.registration")

    type = fields.Char(required=True)
    name = fields.Char()
    phone = fields.Char()


class Registration(models.Model):
    _name = "skts.registration"
    _description = "Registrations"

    state = fields.Selection([
        ("registration", "Registration"),
        ("approved_rejected", "Approved/Rejected"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ], default="approved")

    name = fields.Char(required=True)
    birth_year = fields.Char()
    phone = fields.Char()

    district = fields.Char(required=True)
    neighbourhood = fields.Char(required=True)
    address = fields.Text(required=True)

    note = fields.Text(help="Extra Notes")

    contact_ids = fields.One2many("skts.registration.contact", "registration_id", string="Contacts")

    place_id = fields.Many2one("skts.place", required=True, ondelete="restrict")

    @api.onchange("place_id")
    def _set_type_term(self):
        if self.place_id:
            type_ids = self.place_id.registration_type_ids
            term_ids = self.place_id.term_ids.filtered(lambda r: r.open_to_register is True)
            if len(type_ids) == 1:
                self.type_id = self.place_id.registration_type_ids.id
            if len(term_ids) == 1:
                self.place_term_ids = term_ids

    type_id = fields.Many2one("skts.place.registration.type", string="Registration Type", required=True)

    place_term_ids = fields.Many2many("skts.place.term", "skts_registration_place_term_rel", required=True,
                                       string="Terms", domain="[('place_id', '=', place_id), ('open_to_register', '=', True)]")

    def website_one2many_formatter(self, o2m_field_name, website_context, value):
        o2m_fields = website_context['o2m_fields']
        website_fields = website_context['website_fields']
        o2m_values = []

        for cln_line in website_fields:
            o2m_val = {}
            o2m_line = (0, 0, o2m_val)

            for i in range(len(cln_line)):
                website_field = cln_line[i]
                o2m_field = o2m_fields[i]
                if website_field in value:
                    o2m_val[o2m_field] = value[website_field]
                    del value[website_field]
            if bool(o2m_val):
                o2m_values.append(o2m_line)

        if o2m_values:
            value[o2m_field_name] = o2m_values
        return value

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.id == SUPERUSER_ID:  # Website registration
            vals_list_new = []
            for value in vals_list:
                website_context = json.loads(value['website_context'])
                del value['website_context']
                for field in website_context:
                    if "_ids" in field:
                        value_new = self.website_one2many_formatter(field, website_context[field], value)
                        vals_list_new.append(value_new)
                    else:
                        vals_list_new.append(value)

            return super().create(vals_list_new)

        else:  # Normal registration
            for value in vals_list:
                if not value["place_term_ids"][0][2]:
                    raise UserError(_("You must add at least 1 place term"))
                if not value["contact_ids"]:
                    raise UserError(_("You must add at least 1 contact"))
            res = super().create(vals_list)
            self.env.user.notify_success(message=_('Record created successfully!'))
            return res

    def approve(self):
        self.state = "approved"
