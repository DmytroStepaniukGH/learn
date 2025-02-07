from odoo import models, fields, api
from datetime import timedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation'
    )

    active = fields.Boolean("Active", default=True)

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", efault=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "A property expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "A property selling price must be positive"),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for price in self:
            price.best_price = max(price.offer_ids.mapped("price")) if price.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                min_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_price, precision_rounding=0.01) == -1:
                    raise ValidationError(
                        "Selling price cannot be lower than 90% of the expected price!"
                    )

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError("You cannot cancel a sold property.")
        self.state = 'canceled'

    def action_sell(self):
        if self.state == 'canceled':
            raise UserError("You cannot sell a canceled property.")
        if not self.buyer_id:
            raise UserError("You must accept an offer before selling.")
        self.state = 'sold'