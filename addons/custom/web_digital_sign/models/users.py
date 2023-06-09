# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class RestStaff(models.Model):
    _inherit = 'rest.staff'

    digital_signature = fields.Binary(string='Signature')
