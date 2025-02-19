from odoo import models, fields
from odoo.exceptions import ValidationError


class BillboardRental(models.Model):
    _name = "billboard.rental"
    _description = "Billboard Rental"

    billboard_id = fields.Many2one("billboard", string="Billboard", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], string="Status", default='draft', tracking=True)

    def action_confirm(self):
        for record in self:
            overlapping_rentals = self.env['billboard.rental'].search([
                ('billboard_id', '=', record.billboard_id.id),
                ('state', '=', 'confirmed'),
                ('start_date', '<=', record.end_date),
                ('end_date', '>=', record.start_date),
                ('id', '!=', record.id)
            ])
            if overlapping_rentals:
                raise ValidationError("This billboard is already rented for the selected period.")

            record.state = 'confirmed'