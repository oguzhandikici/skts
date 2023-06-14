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


class SKTSPersonRegistration(models.Model):
    _name = "skts.person.registration"
    _description = "Person Registration"

    person_id = fields.Many2one("skts.person", required=True)

    person_name = fields.Char(related="person_id.name", readonly=False)
    person_surname = fields.Char(related="person_id.surname", readonly=False)
    person_birth_year = fields.Char(related="person_id.birth_year", readonly=False)
    person_phone = fields.Char(related="person_id.phone", readonly=False)
    person_address = fields.Text(related="person_id.address", readonly=False)
    person_district = fields.Char(related="person_id.district", readonly=False)
    person_note = fields.Text(related="person_id.note", readonly=False, string="Person Note")
    person_contact_ids = fields.One2many(related="person_id.contact_ids", readonly=False)

    school_term_ids = fields.One2many("skts.person.registration.school.term", "person_registration_id", required=True, string="School Terms")
    domain_school_term_ids = fields.One2many("skts.school.term", compute="_compute_domain_school_term_ids",
                                             help="Will be used to domain 'school_term_id' inside of 'school_term_ids' to prevent duplicate record creation")

    @api.depends("school_term_ids")
    def _compute_domain_school_term_ids(self):
        self.domain_school_term_ids = self.school_term_ids.mapped("school_term_id")

    school_terms_display = fields.Char(compute="_compute_school_terms_display", string="School Terms")

    @api.depends("school_term_ids")
    def _compute_school_terms_display(self):
        for record in self:
            if record.id:
                computed_name = ''
                if record.school_term_ids:
                    schools = record.school_term_ids.mapped("school_term_id.school_id.name")
                    for school in schools:
                        if computed_name:
                            computed_name += ', '
                        term_names = record.school_term_ids.filtered(lambda r: r.school_term_id.school_id.name == school).mapped("school_term_id.name")
                        computed_name += school + '(' + ' + '.join(term_names) + ')'
                    record.school_terms_display = computed_name
                    return True  # Stop here if all conditions are satisfied
            # else
            record.school_terms_display = False
            return False

    note = fields.Text(string="Registration Note")


class SKTSPersonRegistrationSchoolTerm(models.Model):
    _name = "skts.person.registration.school.term"
    _description = "Person Registration School Terms"

    person_registration_id = fields.Many2one("skts.person.registration", required=True)

    school_term_id = fields.Many2one("skts.school.term", required=True)
    school_term_type_id = fields.Many2one("skts.school.term.type", required=True,
                                          domain="[('school_term_ids', 'in', [school_term_id])]")