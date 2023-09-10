from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RegistrationContact(models.Model):
    _name = "skts.registration.contact"
    _description = "Contacts"

    registration_id = fields.Many2one("skts.registration")

    name = fields.Char(required=True)
    type = fields.Char()
    phone = fields.Char()


class Registration(models.Model):
    _name = "skts.registration"
    _description = "Registrations"

    state = fields.Selection([
        ("registration", "Application"),
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
                self.hide_type = True
            else:
                self.hide_type = False
            if len(term_ids) == 1:
                self.place_term_ids = term_ids
                self.hide_term = True
            else:
                self.hide_term = False

    hide_type = fields.Boolean(compute="_set_type_term")
    hide_term = fields.Boolean(compute="_set_type_term")

    type_id = fields.Many2one("skts.place.registration.type", string="Registration Type", required=True)

    place_term_ids = fields.Many2many("skts.place.term", "skts_registration_place_term_rel", required=True,
                                       string="Terms", domain="[('place_id', '=', place_id), ('open_to_register', '=', True)]")

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list:
            for value in vals_list:
                if not value["place_term_ids"][0][2]:
                    raise UserError(_("You must add at least 1 place term"))
                if not value["contact_ids"]:
                    raise UserError(_("You must add at least 1 contact"))
        return super().create(vals_list)

    def approve(self):
        self.state = "approved"
