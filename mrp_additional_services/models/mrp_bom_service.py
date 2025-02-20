from odoo import models, fields


class MrpBomService(models.Model):
    _name = 'mrp.bom.service'
    _description = 'Additional Services for Bill of Materials'

    bom_id = fields.Many2one('mrp.bom', string="Bill of Materials",
                             required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Service", required=True)
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure",
                                     related="product_id.uom_id", readonly=True)
    quantity = fields.Float(string="Quantity", default=1.0, required=True)