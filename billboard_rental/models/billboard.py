from odoo import models, fields

class Billboard(models.Model):
    _name = "billboard"
    _description = "Billboard"

    name = fields.Char(string="Billboard Name", required=True)
    location = fields.Char(string="Location")
    size = fields.Char(string="Size")
    rent_price = fields.Float(string="Rent Price", help="Price per rental period")