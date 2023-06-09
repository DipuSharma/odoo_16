from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    schedule_assign_user_id = fields.Many2one('res.partner', string="Assign Name")

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('bin_replenishment.schedule_assign_user_id',
                                                         self.schedule_assign_user_id.id)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        BINSudo = self.env['ir.config_parameter'].sudo()
        get_data = BINSudo.get_param('bin_replenishment.schedule_assign_user_id')
        res.update(schedule_assign_user_id=int(get_data) if get_data else False, )
        return res

    # def create(self, vals):
    #     ids = self.env['res.config.settings'].search([])
    #     res = super(BinReplenishmentname, self).create(vals)
    #     if vals.get('bin_replenishmet_Schedule_name'):
    #         for key in ids:
    #             if key.bin_replenishmet_Schedule_name == vals.get('bin_replenishmet_Schedule_name'):
    #                 raise ValidationError(_('Schedule Name already exits.'))
    #     return res
