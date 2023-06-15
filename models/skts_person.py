from odoo import models, fields, api, _


class SKTSPerson(models.Model):
    _name = "skts.person"
    _description = "Persons"
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
    district = fields.Char(required=True)
    note = fields.Text(help="Extra Notes")

    contact_ids = fields.One2many("skts.person.contact", "person_id", string="Contacts")


class SKTSPersonContact(models.Model):
    _name = "skts.person.contact"
    _description = "Person Contacts"

    person_id = fields.Many2one("skts.person")

    name = fields.Char(required=True)
    surname = fields.Char(string="Surname", required=True)
    type = fields.Char()
    phone = fields.Char()
