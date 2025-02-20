from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    additional_services_ids = fields.One2many('mrp.production.service',
                                              'production_id', string="Additional Services")

    @api.onchange('bom_id', 'product_qty')
    def _onchange_bom_id(self):
        if not self.bom_id:
            return

        self.additional_services_ids = [(5, 0, 0)]

        services = []
        for service in self.bom_id.additional_services_ids:
            services.append((0, 0, {
                'product_id': service.product_id.id,
                'quantity': service.quantity * self.product_qty,
            }))

        self.additional_services_ids = services