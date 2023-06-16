from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SKTSPersonRegistration(models.Model):
    _name = "skts.registration"
    _description = "Registrations"

    state = fields.Selection([
        ("application", "Application"),
        ("approved_rejected", "Approved/Rejected"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ], default="application")
    person_id = fields.Many2one("skts.person", required=True)

    person_name = fields.Char(related="person_id.name", readonly=False)
    person_surname = fields.Char(related="person_id.surname", readonly=False)
    person_birth_year = fields.Char(related="person_id.birth_year", readonly=False)
    person_phone = fields.Char(related="person_id.phone", readonly=False)
    person_address = fields.Text(related="person_id.address", readonly=False)
    person_district = fields.Char(related="person_id.district", readonly=False)
    person_note = fields.Text(related="person_id.note", readonly=False, string="Personal Note")
    person_contact_ids = fields.One2many(related="person_id.contact_ids", readonly=False)

    school_id = fields.Many2one("skts.school", required=True, ondelete="restrict")
    type_id = fields.Many2one("skts.school.registration.type", string="Registration Type", required=True)
    school_term_ids = fields.Many2many("skts.school.term", "skts_registration_school_term_rel", required=True,
                                       string="School Terms", domain="[('school_id', '=', school_id), ('open_to_register', '=', True)]")
    school_terms_display = fields.Char(compute="_compute_school_terms_display")
    @api.depends("school_term_ids")
    def _compute_school_terms_display(self):
        for record in self:
            computed_name = ""
            for term_id in record.school_term_ids:
                if computed_name and term_id:
                    computed_name += ' + '
                if term_id:
                    computed_name += term_id.name
            record.school_terms_display = computed_name

    note = fields.Text(string="Registration Note")

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list:
            for value in vals_list:
                if not value["school_term_ids"][0][2]:
                    raise UserError(_("You must add at least 1 school term"))
        return super().create(vals_list)

    def approve(self):
        self.state = "approved"
