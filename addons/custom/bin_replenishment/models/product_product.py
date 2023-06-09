from datetime import date, timedelta
from odoo import fields, models, api

today = date.today()
date_deadline = today + timedelta(days=1)


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product']

    threshold_quantity = fields.Float(string="Threshold QTY", default=f"{30.00}")
    bin_replenishment = fields.Boolean(string="Enable Bin Replenishment", default=False)
    check_qty = fields.Char(string="To Check", compute="check_quantity")

    @api.onchange("threshold_quantity")
    def check_quantity(self):
        for record in self:
            if record.bin_replenishment == 1:
                record.check_qty = "True"
                assign_user = self.env['ir.config_parameter'].sudo().get_param('bin_replenishment'
                                                                               '.schedule_assign_user_id')
                stock_quant = self.env['stock.quant'].search(['&', ('product_id', '=', record.id), ('quantity', '>=', 0)])
                model_id = self.env['ir.model']._get('product.template').id
                mail_activity_type = self.env['mail.activity.type'].search([('name', '=', 'Bin Replenishment')])
                activity_obj = self.env['mail.activity']
                partner_data = self.env['res.users'].search([('partner_id', '=', int(assign_user))])
                print("Product____________________________", stock_quant, model_id, mail_activity_type, activity_obj, partner_data)
        # self.check_qty = "True"
