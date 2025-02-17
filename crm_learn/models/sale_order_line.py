from odoo import models, api
import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Adding order complexity"

    @api.depends('order_id.complexity', 'price_unit', 'discount', 'product_uom_qty', 'tax_id')
    def _compute_amount(self):
        for line in self:
            complexity = line.order_id.complexity
            adjusted_price = line.price_unit * complexity
            price = adjusted_price * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })