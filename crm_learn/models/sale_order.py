from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Complexity of order"

    complexity = fields.Float(string="Complexity", default=1,
                              help="The difficulty factor by which the price is multiplied")