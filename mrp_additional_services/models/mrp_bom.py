from odoo import models, fields, api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    additional_services_ids = fields.One2many('mrp.bom.service', 'bom_id',
                                              string="Additional Services")
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        new_bom = super().copy(default)

        for service in self.additional_services_ids:
            service.copy({'bom_id': new_bom.id})

        return new_bom