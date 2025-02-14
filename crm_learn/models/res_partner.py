import re
from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange('phone', 'mobile')
    def _onchange_format_ukrainian_phone(self):
        for record in self:
            if record.phone:
                record.phone = record._format_ukrainian_phone(record.phone)
            if record.mobile:
                record.mobile = record._format_ukrainian_phone(record.mobile)

    def _format_ukrainian_phone(self, number):
        if not number:
            return ""

        cleaned_number = re.sub(r'\D', '', str(number))

        if cleaned_number.startswith("80") and len(cleaned_number) == 11:
            return f"+380{cleaned_number[2:]}"

        elif cleaned_number.startswith("380") and len(cleaned_number) == 12:
            return f"+{cleaned_number}"

        elif cleaned_number.startswith("0") and len(cleaned_number) == 10:
            return f"+380{cleaned_number[1:]}"

        return number