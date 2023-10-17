from odoo import models, fields, api


class SKTSPlace(models.Model):
    _name = "skts.place"
    _description = "Places"

    name = fields.Char(string="Place Name", required=True)
    website_display_name = fields.Char()

    term_ids = fields.One2many("skts.place.term", "place_id", string="Terms")
    registration_type_ids = fields.One2many("skts.place.registration.type", "place_id", string="Registration Types")

    open_to_register = fields.Boolean(default=True)
    active = fields.Boolean(default=True)


class SKTSPlaceTerm(models.Model):
    _name = "skts.place.term"
    _description = "Place Terms"

    place_id = fields.Many2one("skts.place", required=True)

    registration_ids = fields.Many2many("skts.registration", "skts_registration_term_rel",
                                        "term_id", "registration_id", required=True, string="Registrations")

    color = fields.Integer('Color Index', default=5)
    website_display_name = fields.Char(compute="_compute_website_display_name")

    name = fields.Char(string="Term Name", required=True)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)

    open_to_register = fields.Boolean(default=True)
    show_in_lists = fields.Boolean(default=True)
    active = fields.Boolean(default=True)

    payment_plan_ids = fields.One2many('skts.place.term.payment.plan', 'term_id')

    @api.depends("name", "date_start", "date_end")
    def _compute_website_display_name(self):
        for record in self:
            if record.name and record.date_start and record.date_end:
                date_start = record.date_start.strftime('%d.%m.%Y')
                date_end = record.date_end.strftime('%d.%m.%Y')
                record.website_display_name = record.name + " (" + date_start + " - " + date_end + ")"
            else:
                record.website_display_name = ""


class SKTSPlaceType(models.Model):
    _name = "skts.place.registration.type"
    _description = "Place Registration Types"

    name = fields.Char(required=True)
    place_id = fields.Many2one("skts.place")
