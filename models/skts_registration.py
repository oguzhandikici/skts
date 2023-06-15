from odoo import models, fields, api, _


class SKTSPersonRegistration(models.Model):
    _name = "skts.registration"
    _description = "Registrations"

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
    school_term_ids = fields.Many2many("skts.school.term", "skts_registration_school_term_rel", required=True,
                                       string="School Terms", domain="[('school_id', '=', school_id), ('open_to_register', '=', True)]")
    type_id = fields.Many2one("skts.school.registration.type", string="Registration Type")

    note = fields.Text(string="Registration Note")
