from odoo import models, fields, api


class SKTSPlace(models.Model):
    _name = "skts.place"
    _description = "Places"

    name = fields.Char(string="Place Name", required=True)
    term_ids = fields.One2many("skts.place.term", "place_id", string="Terms")
    registration_type_ids = fields.Many2many("skts.place.registration.type", "skts_place_registration_type_rel", "place_id",
                                             "registration_type_id", string="Registration Types")
    open_to_register = fields.Boolean(default=True)
    active = fields.Boolean(default=True)


class SKTSPlaceTerm(models.Model):
    _name = "skts.place.term"
    _description = "Place Terms"

    place_id = fields.Many2one("skts.place", required=True)

    name = fields.Char(string="Term Name", required=True)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)

    open_to_register = fields.Boolean(default=True)
    active = fields.Boolean(default=True)

    registration_ids = fields.Many2many("skts.registration", "skts_registration_term_rel",
                                        "term_id", "registration_id", required=True, string="Registrations")


class SKTSPlaceTermType(models.Model):
    _name = "skts.place.registration.type"
    _description = "Place Registration Types"

    name = fields.Char(required=True)
    place_ids = fields.Many2many("skts.place", "skts_place_registration_type_rel", "registration_type_id",
                                  "place_id", string="Places")
