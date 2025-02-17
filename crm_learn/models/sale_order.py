from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Complexity of order"

    complexity = fields.Float(string="Complexity", default=1,
                              help="The difficulty factor by which the price is multiplied")

    @api.depends('order_line', 'order_line.price_subtotal', 'order_line.price_tax', 'complexity')
    def _amount_all(self):
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_line) * order.complexity
            amount_tax = sum(line.price_tax for line in order.order_line) * order.complexity

            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = amount_untaxed + amount_tax

            _logger.info(f"Order {order.name}: Complexity={order.complexity}, "
                         f"Untaxed={amount_untaxed}, Tax={amount_tax}, Total={amount_untaxed + amount_tax}")