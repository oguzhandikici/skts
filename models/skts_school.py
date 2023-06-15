from odoo import models, fields, api


class SKTSSchool(models.Model):
    _name = "skts.school"
    _description = "Schools"

    name = fields.Char(string="School Name", required=True)
    term_ids = fields.One2many("skts.school.term", "school_id", string="Terms")
    registration_type_ids = fields.Many2many("skts.school.registration.type", "skts_school_registration_type_rel", "school_id",
                                             "registration_type_id", string="Registration Types",
                                             default=lambda self: self.env["skts.school.registration.type"].search([]))

    active = fields.Boolean(default=True)


class SKTSSchoolTerm(models.Model):
    _name = "skts.school.term"
    _description = "School Terms"

    school_id = fields.Many2one("skts.school", required=True)

    name = fields.Char(string="Term Name", required=True)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)

    open_to_register = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    registration_ids = fields.Many2many("skts.registration", "skts_registration_term_rel",
                                        "term_id", "registration_id", required=True, string="Registrations")


class SKTSSchoolTermType(models.Model):
    _name = "skts.school.registration.type"
    _description = "School Registration Types"

    name = fields.Char(required=True)
    school_ids = fields.Many2many("skts.school", "skts_school_registration_type_rel", "registration_type_id",
                                  "school_id", string="Schools")
