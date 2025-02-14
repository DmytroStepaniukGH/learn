from odoo import models, fields


class ClientRisk(models.Model):
    _name = "client.risk"
    _description = "The degree of risk of the client"

    name = fields.Char(string="Risk Level", required=True)

    def action_set_client_risk(self):

        lead_id = self.env.context.get("active_id")

        if lead_id:
            lead = self.env["crm.lead"].browse(lead_id)
            lead.client_risk_id = self.client_risk_id