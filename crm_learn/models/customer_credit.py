from odoo import models, fields, api


class CustomerCredit(models.Model):
    _name = "customer.credit"
    _description = "Customer Credit"

    _inherit = ['mail.thread', 'mail.activity.mixin']

    date_issued = fields.Date(string="Date Issued", default=fields.Date.today(), required=True)
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    credit_amount = fields.Float(string="Credit Amount", required=True, tracking=True)
    interest_rate = fields.Float(string="Interest Rate (%)", required=True, tracking=True)
    interest_amount = fields.Float(string="Interest Amount", compute="_compute_interest_amount",
                                   store=True, track_visibility="onchange")

    @api.depends("credit_amount", "interest_rate")
    def _compute_interest_amount(self):
        for record in self:
            record.interest_amount = (record.credit_amount * record.interest_rate) / 100 \
                if record.credit_amount and record.interest_rate else 0