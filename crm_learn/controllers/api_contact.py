import json
from odoo import http
from odoo.http import request


class ContactAPI(http.Controller):

    @http.route('/api/add_contact', type='http', auth='public', methods=['GET'], csrf=False)
    def add_contact(self, name=None, phone=None, **kwargs):

        if not name or not phone:
            return json.dumps({'error': 'Missing required parameters: name, phone'}), 400

        existing_contact = request.env['res.partner'].sudo().search([('phone', '=', phone)], limit=1)

        if existing_contact:
            return json.dumps({'message': 'Contact already exists ', 'id': existing_contact.id})

        new_contact = request.env['res.partner'].sudo().create({
            'name': name,
            'phone': phone,
        })

        return json.dumps({'message': 'Contact created successfully ', 'id': new_contact.id})