from odoo import models, api, fields
import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Adding order complexity"

    complexity = fields.Float(related="order_id.complexity", store=True)

    #not work - need fix
    @api.onchange('product_id')
    def _onchange_product_id(self):
        _logger.info("ONCHANGE product_id ВИКЛИКАНО")

        self.price_unit = self.price_unit * self.complexity
        _logger.info(f"Новий price_unit: {self.price_unit} для {self.product_id.name}")