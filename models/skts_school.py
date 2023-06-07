from odoo import models, fields


class SKTSSchool(models.Model):
    _name = "skts.school"
    _description = "Schools"

    name = fields.Char(string="School Name")
    term_ids = fields.One2many("skts.school.term", "school_id")

    active = fields.Boolean(default=True)


class SKTSSchoolTerm(models.Model):
    _name = "skts.school.term"
    _description = "School Terms"

    school_id = fields.Many2one("skts.school", required=True)

    name = fields.Char(string="Term Name", required=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")

    active = fields.Boolean(default=True)
