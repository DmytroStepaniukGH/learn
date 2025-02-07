from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer("Sequence", default=1)

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]