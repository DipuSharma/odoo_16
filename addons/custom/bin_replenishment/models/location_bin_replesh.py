from odoo import fields, models, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError

today = date.today()
date_deadline = today + timedelta(days=1)


class MailActivity(models.Model):
    _name = 'mail.activity'
    _inherit = ['mail.activity']
    loc_name = fields.Char(string="Location Name")


class StockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['stock.quant']

    stock_quantity_check = fields.Char("Stock Quantity", compute="stock_quantity")

    @api.model
    def stock_quantity(self):
        for rec in self:
            if rec.location_id.usage == 'internal' and rec.location_id.active == True:
                location_data = self.env['stock.location'].search(
                    ['&', '&', ('id', '=', rec.location_id.id), ('bin_replenishment', '=', True),
                     ('complete_name', 'ilike', '-R-0'), ('exclude_rules', '=', False)])
                if location_data:
                    mail_activity_data = self.env['mail.activity'].search(
                        ['&', ('res_name', 'ilike', rec.product_id.name),
                         ('loc_name', '=', rec.location_id.complete_name)])
                    assign_user = self.env['ir.config_parameter'].search([('key', '=', 'bin_replenishment'
                                                                                       '.schedule_assign_user_id')])[-1]
                    mail_activity_type = self.env['mail.activity.type'].search([('name', '=', 'Bin Replenishment')])
                    partner_data = self.env['res.users'].search([('partner_id', '=', int(assign_user.value))])
                    model_id = self.env['ir.model']._get('product.template').id
                    activity_obj = self.env['mail.activity']
                    if location_data and rec.quantity <= location_data.thresh_quantity:
                        if not mail_activity_data:
                            activity_obj.create({'res_id': rec.product_id.product_tmpl_id, 'res_model_id': model_id,
                                                 'activity_type_id': mail_activity_type.id,
                                                 'date_deadline': date_deadline,
                                                 'note': f"<p>This schedule activity for location based "
                                                         f"({rec.location_id.complete_name}) product name is "
                                                         f"{rec.product_id.name} <p>",
                                                 'user_id': partner_data.id,
                                                 'loc_name': rec.location_id.complete_name})
                    if location_data and rec.quantity > location_data.thresh_quantity:
                        for activity_data in mail_activity_data:
                            activity_data.action_feedback_schedule_next()
        self.stock_quantity_check = "True"


class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['stock.location', 'mail.thread', 'mail.activity.mixin']

    thresh_quantity = fields.Float(string="Threshold QTY", default=f"{30.00}")
    bin_replenishment = fields.Boolean(string="Enable Bin Replenishment", default=False)
    exclude_rules = fields.Boolean(string="Exclude from rules", default=False)
    # check_qty = fields.Char(string="To Check", compute="check_quantity")

    # @api.model
    # def check_quantity(self):
    #     for rec in self:
    #         rec.check_qty = "True"
    #         if rec.active == 1 and rec.bin_replenishment == 1:
    #             try:
    #                 get_user_data = self.env['res.config.settings'].search([])[-1]
    #             except:
    #                 raise ValidationError(_("Assign name not found please choose in Settings -> Bin Replenishment "))
    #             mail_activity_type = self.env['mail.activity.type'].search([])
    #             stock_quant = self.env['stock.quant'].search([('location_id', '=', rec.id)])
    #             # mail_activity_data = self.env['mail.activity'].search([('res_name', 'like', rec.complete_name)])
    #             model_id = self.env['ir.model']._get('product.template').id
    #             partner_data = self.env['res.users'].search(
    #                 [('partner_id', '=', get_user_data.schedule_assign_user_id.id)])
    #             activity_obj = self.env['mail.activity']
    #             activity_id = []
    #             for record in mail_activity_type:
    #                 if record.name == 'Bin Replenishment':
    #                     activity_id.append(record.id)
    #             for data in stock_quant:
    #                 mail_activity_data = self.env['mail.activity'].search([('res_name', 'like', data.product_id.name)])
    #                 if rec.thres_quantity >= data.quantity:
    #                     if not mail_activity_data:
    #                         activity_obj.create({'res_id': data.product_id.product_tmpl_id, 'res_model_id': model_id,
    #                                              'activity_type_id': activity_id[0],
    #                                              'date_deadline': date_deadline,
    #                                              'note': f"<p>This schedule activity for location based ({rec.complete_name}) product name is {data.product_id.name} <p>",
    #                                              'user_id': partner_data.id})
    #                 if rec.thres_quantity < data.quantity:
    #                     for record_data in mail_activity_data:
    #                         record_data.action_feedback_schedule_next()
