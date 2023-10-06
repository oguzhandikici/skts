from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools.misc import groupby
import json


class RegistrationContact(models.Model):
    _name = "skts.registration.contact"
    _description = "Contacts"
    _order = "registration_id, sequence asc"

    registration_id = fields.Many2one("skts.registration")

    sequence = fields.Integer(default=1)
    type = fields.Char(required=True)
    name = fields.Char()
    phone = fields.Char(required=True)

    action_html = fields.Html(compute="_compute_action_html")
    invisible_down = fields.Boolean(compute="_compute_invisible_up_down")
    invisible_up = fields.Boolean(compute="_compute_invisible_up_down")

    def action_get_contact_form(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': self._name,
            'target': 'new',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for value in vals_list:
            new_sequence = len(self.env['skts.registration'].browse([value['registration_id']]).contact_ids)
            value['sequence'] = new_sequence
        return super().create(vals_list)

    @api.depends("invisible_down", "invisible_up")
    def _compute_invisible_up_down(self):
        for record in self:
            invisible_up, invisible_down = True, True
            contact_ids = record.registration_id.contact_ids.sorted('sequence')
            if len(contact_ids) > 1:
                if contact_ids[0].sequence < record.sequence < contact_ids[-1].sequence:
                    invisible_up, invisible_down = False, False
                elif record == contact_ids[-1]:
                    invisible_up, invisible_down = False, True
                elif record == contact_ids[0]:
                    invisible_up, invisible_down = True, False
            else:
                invisible_up, invisible_down = True, True

            record.invisible_up, record.invisible_down = invisible_up, invisible_down

    @api.depends("phone")
    def _compute_action_html(self):
        for record in self:
            if record.phone:
                tel = f'<a href="tel:{record.phone}" class="fa fa-phone fa-lg" title="TEL: {record.type}"/>'
                sms = f'<a href="sms:{record.phone}" class="fa fa-sms fa-lg" style="padding-left: 14px;" title="SMS: {record.type}"/>'
                whatsapp = f'<a href="https://wa.me/{record.phone}" class="fab fa-whatsapp fa-lg" style="padding-left: 14px;" title="WP: {record.type}"/>'
                record.action_html = tel + sms + whatsapp
            else:
                record.action_html = ''

    def change_sequence_mobile(self):
        type = self.env.context.get('type')
        sequence = getattr(self, 'sequence')

        if type == 'down':
            records = self.registration_id.contact_ids.filtered(lambda r: r.sequence in [sequence, sequence+1])

            self.sequence = sequence + 1
            records[1].sequence = sequence

        elif type == 'up':
            records = self.registration_id.contact_ids.filtered(lambda r: r.sequence in [sequence, sequence-1])

            self.sequence = self.sequence - 1
            records[0].sequence = sequence


class Registration(models.Model):
    _name = "skts.registration"
    _description = "Registrations"

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ("awaiting_registration", "Awaiting Registration"),
        ("registered", "Registered"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ], default="registered")

    name = fields.Char(required=True)
    birth_year = fields.Char()
    phone = fields.Char()
    district = fields.Char(required=True)
    neighbourhood = fields.Char(required=True)
    address = fields.Text(required=True)
    full_address = fields.Text(compute="_compute_full_address")
    note = fields.Text(help="Extra Notes")
    contact_ids = fields.One2many("skts.registration.contact", "registration_id", string="Contacts")
    contact_html = fields.Html(compute="_compute_contact_html")

    place_id = fields.Many2one("skts.place", required=True, ondelete="restrict")
    type_id = fields.Many2one("skts.place.registration.type", string="Registration Type", required=True)
    place_term_ids = fields.Many2many("skts.place.term", "skts_registration_place_term_rel", required=True,
                                       string="Terms", domain="[('place_id', '=', place_id), ('open_to_register', '=', True)]")

    morning_driver_id = fields.Many2one("skts.driver", group_expand="_group_expand_drivers")
    morning_hour = fields.Float(group_operator=False)
    morning_sequence = fields.Integer(default=1, group_operator=False)
    morning_seat_state = fields.Selection([
        ('below_seat_limit', 'Below Seat Limit'),
        ('full', 'Full'),
        ('above_seat_limit', 'Above Seat Limit'),
    ], compute="_compute_morning_seat_state")

    evening_driver_id = fields.Many2one("skts.driver", group_expand="_group_expand_drivers")
    evening_hour = fields.Float(group_operator=False)
    evening_sequence = fields.Integer(default=1, group_operator=False)
    evening_seat_state = fields.Selection([
        ('below_seat_limit', 'Below Seat Limit'),
        ('full', 'Full'),
        ('above_seat_limit', 'Above Seat Limit'),
    ], compute="_compute_evening_seat_state")

    payment_ids = fields.One2many("skts.payment", "registration_id", string="Payments")


    @api.depends("morning_driver_id.seats", "morning_driver_id")
    def _compute_morning_seat_state(self):
        driver_group = {
            driver: {
                'registrations': list(registrations),
                'seat_limit': driver.seats
            } for driver, registrations in groupby(self, lambda x: x.morning_driver_id)
        }
        for driver in driver_group:
            driver_registrations = driver_group[driver]['registrations']
            driver_seats = driver_group[driver]['seat_limit']
            full_seats = len(driver_registrations)

            if full_seats > driver_seats:
                for r in driver_registrations[0:driver_seats]:
                    r.morning_seat_state = 'full'
                for r in driver_registrations[driver_seats:]:
                    r.morning_seat_state = 'above_seat_limit'
            elif full_seats < driver_seats:
                for r in driver_registrations:
                    r.morning_seat_state = 'below_seat_limit'
            elif full_seats == driver_seats:
                for r in driver_registrations:
                    r.morning_seat_state = 'full'

    @api.depends("evening_driver_id.seats", "evening_driver_id")
    def _compute_evening_seat_state(self):
        driver_group = {
            driver: {
                'registrations': list(registrations),
                'seat_limit': driver.seats
            } for driver, registrations in groupby(self, lambda x: x.evening_driver_id)
        }
        for driver in driver_group:
            driver_registrations = driver_group[driver]['registrations']
            driver_seats = driver_group[driver]['seat_limit']
            full_seats = len(driver_registrations)

            if full_seats > driver_seats:
                for r in driver_registrations[0:driver_seats]:
                    r.evening_seat_state = 'full'
                for r in driver_registrations[driver_seats:]:
                    r.evening_seat_state = 'above_seat_limit'
            elif full_seats < driver_seats:
                for r in driver_registrations:
                    r.evening_seat_state = 'below_seat_limit'
            elif full_seats == driver_seats:
                for r in driver_registrations:
                    r.evening_seat_state = 'full'

    @api.model
    def _group_expand_drivers(self, stages, domain, order):
        if not self.env.context.get("mylist_view"):
            return self.env['skts.driver'].search([], order=order)
        else:
            return stages

    @api.depends("full_address")
    def _compute_full_address(self):
        for record in self:
            if record.neighbourhood and record.address and record.district:
                record.full_address = f"{record.neighbourhood}, {record.address}, {record.district}"
            else:
                record.full_address = ""

    def open_map(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'https://maps.google.com/maps?q={self.full_address}',
        }

    @api.depends("contact_ids")
    def _compute_contact_html(self):
        for record in self:
            html = ""
            count = 0
            limit = len(record.contact_ids)-1
            sorted_contact_ids = record.contact_ids.sorted("sequence", reverse=True)  # Butonlar sağdan sola oluştuğu için ters sıralanıyor
            for contact_id in sorted_contact_ids:
                padding_right = "padding-right: 20px;" if count > 0 else "padding-right: 5px;"
                icon = "far fa-phone" if count < limit else "fa fa-phone"
                html += f'<a href="tel:{contact_id.phone}" target="_self" style="{padding_right}" class="{icon} fa-lg oe_kanban_action oe_kanban_action_a float-end" title="TEL: {contact_id.type}"/>'
                count += 1
            record.contact_html = html

    @api.onchange("place_id")
    def _set_type_term(self):
        if self.place_id:
            self.type_id = False
            self.place_term_ids = False
            type_ids = self.place_id.registration_type_ids
            term_ids = self.place_id.term_ids.filtered(lambda r: r.open_to_register is True)
            if len(type_ids) == 1:
                self.type_id = self.place_id.registration_type_ids.id
            if len(term_ids) == 1:
                self.place_term_ids = term_ids

    def website_one2many_formatter(self, o2m_field_name, website_context, value):
        o2m_fields = website_context['o2m_fields']
        website_fields = website_context['website_fields']
        o2m_values = []

        for cln_line in website_fields:
            o2m_val = {}
            o2m_line = (0, 0, o2m_val)

            for i in range(len(cln_line)):
                website_field = cln_line[i]
                o2m_field = o2m_fields[i]
                if website_field in value:
                    o2m_val[o2m_field] = value[website_field]
                    del value[website_field]
            if bool(o2m_val):
                o2m_values.append(o2m_line)

        if o2m_values:
            value[o2m_field_name] = o2m_values
        return value

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.id == SUPERUSER_ID:  # Website registration
            vals_list_new = []
            for value in vals_list:
                website_context = json.loads(value['website_context'])
                del value['website_context']
                for field in website_context:
                    if "_ids" in field:
                        value_new = self.website_one2many_formatter(field, website_context[field], value)
                        vals_list_new.append(value_new)
                    else:
                        vals_list_new.append(value)

            return super().create(vals_list_new)

        else:  # Normal registration
            for value in vals_list:
                if not value["place_term_ids"][0][2]:
                    raise UserError(_("You must add at least 1 place term"))
                if not value["contact_ids"]:
                    raise UserError(_("You must add at least 1 contact"))
            res = super().create(vals_list)
            self.env.user.notify_success(message=_('Record created successfully!'))
            return res

    def approve(self):
        self.write({'state': "registered", 'active': True})

    def reject(self):
        if self.state == 'awaiting_registration':
            self.write({'state': "rejected", 'active': False})
        elif self.state == 'registered':
            self.write({'state': "cancelled", 'active': False})

    def unlink(self):
        if self.state == 'registered':
            raise UserError(_("You need to Cancel this record before deleting."))
