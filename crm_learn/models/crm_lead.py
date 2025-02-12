from odoo import models, fields, api
from datetime import date

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    days_in_work = fields.Integer(
        string='Днів в роботі',
        compute='_compute_days_in_work',
        store=True
    )

    @api.depends('create_date')
    def _compute_days_in_work(self):
        for lead in self:
            if lead.create_date:
                lead.days_in_work = (date.today() - lead.create_date.date()).days
            else:
                lead.days_in_work = 0