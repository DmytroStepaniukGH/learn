from odoo import models, fields, api

class ClientRiskWizard(models.TransientModel):
    _name = "client.risk.wizard"
    _description = "Wizard for choosing the degree of risk of the client"

    client_risk_id = fields.Many2one(
        comodel_name="client.risk",
        string="The degree of risk of the client",
        required=True
    )

    def apply_risk_level(self):
        lead_id = self.env.context.get("active_id")

        if lead_id:
            lead = self.env["crm.lead"].browse(lead_id)
            lead.client_risk_id = self.client_risk_id