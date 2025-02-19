import urllib.request
import urllib.parse

import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    days_in_work = fields.Integer(string='Days at work', compute='_compute_days_in_work')
    client_risk_id = fields.Many2one(comodel_name="client.risk", string="The degree of risk of the client")

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

    @api.model
    def create(self, vals):
        lead = super(CrmLead, self).create(vals)
        lead._send_telegram_notification()
        return lead

    def _send_telegram_notification(self):
        company = self.env.company
        token = company.telegram_token

        if not token:
            return

        message_text = f"New CRM Lead: {self.name}"

        chats = self.env['telegram.chat'].search([('send_messages', '=', True)])

        for chat in chats:
            chat_id = chat.chat_id
            params = urllib.parse.urlencode({
                'chat_id': chat_id,
                'text': message_text,
            })
            url = f"https://api.telegram.org/bot{token}/sendMessage?{params}"
            try:
                urllib.request.urlopen(url)
            except Exception as e:
                _logger.error(f"Error sending Telegram message to chat {chat_id}: {e}")