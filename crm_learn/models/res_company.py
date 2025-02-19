import json
import urllib.request
import urllib.parse
import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    telegram_token = fields.Char(string="Telegram Token")
    telegram_chat_count = fields.Integer(string="Telegram Chats", compute="_compute_telegram_chat_count")


    def _compute_telegram_chat_count(self):
        for company in self:
            company.telegram_chat_count = self.env['telegram.chat'].search_count([])

    def action_get_incoming_messages(self):
        self.ensure_one()

        url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            raise Exception(f"Error fetching Telegram updates: {e}")

        telegram_chat = self.env['telegram.chat']
        for update in data.get('result', []):
            message = update.get('message') or update.get('edited_message')

            if not message:
                continue

            chat = message.get('chat')

            if not chat:
                continue

            chat_id = str(chat.get('id'))
            username = chat.get('username') or chat.get('first_name') or "Unknown"
            existing = telegram_chat.search([('chat_id', '=', chat_id)], limit=1)

            if existing:
                existing.write({'telegram_username': username, 'send_messages': True})
            else:
                telegram_chat.create({'telegram_username': username, 'chat_id': chat_id, 'send_messages': True})

        return True