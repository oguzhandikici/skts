from odoo import models, fields


class SKTSStudent(models.Model):
    _name = "skts.student"
    _description = "Students"

    name = fields.Char(string="Name")
    surname = fields.Char(string="Surname")
    birth_year = fields.Char()
    phone_number = fields.Char()
    address = fields.Text()
    district = fields.Char()

    contact_ids = fields.One2many("skts.student.contact", "student_id")


class SKTSStudentContact(models.Model):
    _name = "skts.student.contact"
    _description = "Student Contacts"

    student_id = fields.Many2one("skts.student")

    name = fields.Char(string="Name")
    surname = fields.Char(string="Surname")
    type = fields.Selection([("mother", "Mother"), ("father", "Father"), ("companion", "Companion")])


class SKTSStudentRegistration(models.Model):
    _name = "skts.student.registration"
    _description = "Student Registration"

    student_id = fields.Many2one("skts.student")  # Öğrenci önceden kayıtlıysa seç, yoksa oluştur.
    school_term_id = fields.Many2one("skts.school.term")
    type = fields.Selection([
        ("full_time", "Full Time"),
        ("half_time", "Half Time"),
    ], default="full_time")
