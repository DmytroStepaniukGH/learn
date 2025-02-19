from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('price_unit')
    def _onchange_price(self):
        complexity = self.order_id.complexity

        if self.price_unit and not self._context.get('onchange_price_done'):
            self = self.with_context(onchange_price_done=True)  # Prevents infinite loop
            self.price_unit = self.price_unit * complexity