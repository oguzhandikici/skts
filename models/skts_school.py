from odoo import models, fields, api


class SKTSSchool(models.Model):
    _name = "skts.school"
    _description = "Schools"

    name = fields.Char(string="School Name", required=True)
    term_ids = fields.One2many("skts.school.term", "school_id", string="Terms", ondelete="restrict")

    active = fields.Boolean(default=True)


class SKTSSchoolTerm(models.Model):
    _name = "skts.school.term"
    _description = "School Terms"
    _rec_name = "school_term_name"

    school_id = fields.Many2one("skts.school", required=True)
    school_term_name = fields.Char(compute="_compute_school_term_name", search="_search_school_term_name")
    @api.depends("name", "school_id")
    def _compute_school_term_name(self):
        for record in self:
            if record.id:
                record.school_term_name = record.school_id.name + ' ' + '(' + record.name + ')'
            else:
                record.school_term_name = False

    def _search_school_term_name(self, operator, value):
        return ['|', ('name', operator, value), ('school_id.name', operator, value)]

    name = fields.Char(string="Term Name", required=True)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)
    type_ids = fields.Many2many("skts.school.term.type", "skts_school_term_type_rel", "school_term_id", "term_type_id",
                                string="Types", default=lambda self: self.env['skts.school.term.type'].search([]).ids)

    open_to_register = fields.Boolean(default=False)
    active = fields.Boolean(default=True)


    registration_ids = fields.Many2many("skts.person.registration", "skts_person_registration_term_rel",
                                        "term_id", "registration_id", required=True, string="Registrations")



class SKTSSchoolTermType(models.Model):
    _name = "skts.school.term.type"
    _description = "School Term Types"

    name = fields.Char(required=True)
    school_term_ids = fields.Many2many("skts.school.term", "skts_school_term_type_rel", "term_type_id",
                                       "school_term_id", string="School Terms")
