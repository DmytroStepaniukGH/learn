import requests
import logging
from odoo import models, fields, api


_logger = logging.getLogger(__name__)

class CurrencyRateUpdate(models.Model):
    _inherit = "res.currency"

    @api.model
    def update_currency_rates(self):
        """ Оновлення курсу валют НБУ та запис у res.currency.rate """
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()

                currencies = {'USD': None, 'EUR': None}
                for currency in data:
                    if currency['cc'] in currencies:
                        currencies[currency['cc']] = currency['rate']

                for currency_code, rate in currencies.items():
                    if rate:
                        currency = self.env['res.currency'].search([('name', '=', currency_code)], limit=1)

                        if not currency:
                            _logger.warning(f"Currency {currency_code} not found")
                            continue

                        existing_rate = self.env['res.currency.rate'].search([
                            ('currency_id', '=', currency.id),
                            ('name', '=', fields.Date.today()),
                        ], limit=1)

                        if existing_rate:
                            existing_rate.write({'rate': 1 / rate})
                            _logger.info(f"Currency {currency_code} updated: {rate}")
                        else:
                            self.env['res.currency.rate'].create({
                                'currency_id': currency.id,
                                'rate': 1 / rate,
                                'name': fields.Date.today()
                            })
                            self.env.cr.commit()
                            _logger.info(f"Rate {currency_code} added: {rate}")

            else:
                _logger.error(f"Error request: {response.status_code}")

        except requests.RequestException as e:
            _logger.critical(f"Error in request to NBU: {str(e)}")