from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one("estate.property.type",
                                       related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer price must be strictly positive"),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + timedelta(offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_accept(self):
        if self.property_id.state == 'sold':
            raise UserError("You cannot accept an offer for a sold property.")

        existing_accepted = self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
        if existing_accepted:
            raise UserError("There is already an accepted offer for this property.")

        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        self.status = 'refused'
        self.property_id.state = 'canceled'