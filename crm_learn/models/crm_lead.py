from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    days_in_work = fields.Integer(string='Днів в роботі', compute='_compute_days_in_work', store=True)

    client_risk_id = fields.Many2one(comodel_name="client.risk", string="Ступінь ризику клієнта")

    @api.depends('create_date')
    def _compute_days_in_work(self):
        for lead in self:
            if lead.create_date:
                lead.days_in_work = (fields.Date.today() - lead.create_date.date()).days
            else:
                lead.days_in_work = 0

    def action_open_client_risk_wizard(self):
        return {
            "name": "Set Client Risk Level",
            "type": "ir.actions.act_window",
            "res_model": "client.risk.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_client_risk_id": self.client_risk_id.id},
        }