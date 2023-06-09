from odoo import fields, models, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError

today = date.today()
date_deadline = today + timedelta(days=1)


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template']

    thresh_quantity = fields.Float(string="Threshold QTY", default=f"{30.00}")
    bin_replenishment = fields.Boolean(string="Enable Bin Replenishment", default=False)
    exclude_rules = fields.Boolean(string="Exclude from rules")
    check_qty = fields.Char(string="To Check", compute="check_quantity")

    @api.onchange("thres_quantity")
    def check_quantity(self):
        for rec in self:
            if rec.bin_replenishment == 1:
                assign_user = self.env['ir.config_parameter'].sudo().get_param(
                    'bin_replenishment.schedule_assign_user_id')
                product_ids = self.env['product.product'].search([('product_tmpl_id', '=', rec.id)])
                stock_quant = self.env['stock.quant'].search(
                    ['&', ('product_id', '=', product_ids.id), ('quantity', '>=', 0)])
                model_id = self.env['ir.model']._get('product.template').id
                mail_activity_type = self.env['mail.activity.type'].search([('name', '=', 'Bin Replenishment')])
                activity_obj = self.env['mail.activity']
                partner_data = self.env['res.users'].search([('partner_id', '=', int(assign_user))])
                if not assign_user:
                    raise ValidationError(
                        _("Assign name is not found please choose in Settings -> Inventory -> Bin Replenishment -> "
                          "Choos user "))
                for data in stock_quant:
                    mail_activity_data = \
                        self.env['mail.activity'].search(['&', ('res_name', 'ilike', rec.name),
                                                          ('loc_name', '=', data.location_id.complete_name)])
                    location_data = self.env['stock.location'].search(
                        ['&', '&', ('complete_name', 'ilike', '-R-0'), ('exclude_rules', '=', False),
                         ('id', '=', data.location_id.id)])
                    if data.location_id.usage == 'internal' and data.location_id.active == True and location_data:
                        if rec.thresh_quantity >= data.quantity:
                            if not mail_activity_data:
                                activity_obj.create(
                                    {'res_id': rec.id, 'res_model_id': model_id,
                                     'activity_type_id': mail_activity_type.id,
                                     'date_deadline': date_deadline,
                                     'note': f"<p>This schedule activity for product based, product name is {rec.name} "
                                             f"and location name is ({data.location_id.complete_name})<p>",
                                     'user_id': partner_data.id,
                                     'loc_name': data.location_id.complete_name
                                     })
                        if rec.thresh_quantity < data.quantity:
                            if mail_activity_data:
                                mail_activity_data.action_feedback_schedule_next()
            rec.check_qty = "True"

# else:
#     for data in mail_activity_data:
#         if today < data.date_deadline and self.name in data.res_name:
#             pass
#         if today == data.date_deadline and self.name in data.res_name:
#             pass
#         if today > data.date_deadline and self.name in data.res_name:
#             data.write({'id': data.id, 'res_id': self.id, 'res_model_id': model_id,
#                         'activity_type_id': activity_id[0],
#                         'date_deadline': date_deadline,
#                         'note': f"<p>This Schedule Activity <p>",
#                         'user_id': user_id[0]})
