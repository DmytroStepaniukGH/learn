from odoo import models, fields


class MrpProductionService(models.Model):
    _name = 'mrp.production.service'
    _description = 'Additional Services for Manufacturing Orders'

    production_id = fields.Many2one('mrp.production', string="Manufacturing Order",
                                    required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Service", required=True)
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure",
                                     related="product_id.uom_id", readonly=True)
    quantity = fields.Float(string="Quantity", default=1.0, required=True)