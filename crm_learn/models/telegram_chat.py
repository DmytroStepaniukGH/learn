from odoo import models, fields


class TelegramChat(models.Model):
    _name = "telegram.chat"
    _description = "Telegram Chat"

    telegram_username = fields.Char(string="Telegram Username")
    chat_id = fields.Char(string="Chat ID", required=True)
    send_messages = fields.Boolean(string="Send Messages", default=False)