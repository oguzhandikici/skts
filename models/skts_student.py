from odoo import models, fields, api, _


class SKTSStudent(models.Model):
    _name = "skts.student"
    _description = "Students"
    _rec_name = "full_name"

    full_name = fields.Char(compute="_compute_full_name", search="_search_full_name")
    # TODO: Her veli sadece kendi çocuğunu görebilmeli, user veya benzeri bir mekanizma eklenecek.
    @api.depends("name", "surname")
    def _compute_full_name(self):
        for record in self:
            if record.id:
                record.full_name = record.name + ' ' + record.surname
            else:
                record.full_name = False

    def _search_full_name(self, operator, value):
        return ['|', ('name', operator, value), ('surname', operator, value)]

    name = fields.Char(required=True)
    surname = fields.Char(string="Surname", required=True)
    birth_year = fields.Char()
    phone = fields.Char()
    address = fields.Text(required=True)
    district = fields.Char()
    note = fields.Text(help="Extra Notes")

    contact_ids = fields.One2many("skts.student.contact", "student_id", string="Contacts")


class SKTSStudentContact(models.Model):
    _name = "skts.student.contact"
    _description = "Student Contacts"

    student_id = fields.Many2one("skts.student")

    name = fields.Char(required=True)
    surname = fields.Char(string="Surname", required=True)
    type = fields.Selection([("mother", "Mother"), ("father", "Father"), ("companion", "Companion")])
    phone = fields.Char()


class SKTSStudentRegistration(models.Model):
    _name = "skts.student.registration"
    _description = "Student Registration"

    student_id = fields.Many2one("skts.student", required=True)

    student_name = fields.Char(related="student_id.name", readonly=False)
    student_surname = fields.Char(related="student_id.surname", readonly=False)
    student_birth_year = fields.Char(related="student_id.birth_year", readonly=False)
    student_phone = fields.Char(related="student_id.phone", readonly=False)
    student_address = fields.Text(related="student_id.address", readonly=False)
    student_district = fields.Char(related="student_id.district", readonly=False)
    student_note = fields.Text(related="student_id.note", readonly=False)

    student_contact_ids = fields.One2many(related="student_id.contact_ids")
    school_term_ids = fields.Many2many("skts.school.term", "skts_student_registration_term",
                                       "registration_id", "term_id", required=True, string="School Terms")
    type = fields.Selection([
        ("full_time", "Full Time"),
        ("half_time", "Half Time"),
    ], default="full_time", required=True)

    note = fields.Text()
