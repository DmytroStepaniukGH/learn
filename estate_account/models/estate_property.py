from odoo import models, fields, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        result = super(EstateProperty, self).action_sell()

        partner_id = self.buyer_id.id
        move_type = 'out_invoice'
        journal_id = self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id

        selling_price = self.selling_price
        commission = selling_price * 0.06
        admin_fees = 100.00


        if partner_id and journal_id:
            self.env['account.move'].create({
                'partner_id': partner_id,
                'move_type': move_type,
                'journal_id': journal_id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Комісія за продаж (6%)',
                        'quantity': 1,
                        'price_unit': commission,
                    }),
                    Command.create({
                        'name': 'Адміністративні збори',
                        'quantity': 1,
                        'price_unit': admin_fees,
                    }),
                ],
            })

        return result