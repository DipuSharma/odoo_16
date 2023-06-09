from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(string="Api Key")

    @api.model
    def create(self, vals):
        ids = self.env['res.config.settings'].search([])
        res = super(ResConfigSettings, self).create(vals)
        if vals.get('api_key'):
            for key in ids:
                if key.api_key == vals.get('api_key'):
                    raise ValidationError(_('Api Key Already Existed.'))
        return res
