from pyexpat import model
from odoo import fields, models, api, _


class VendorGrade(models.Model):
    _name = "vendor.grade"
    _description = "This model use for vendor grading"
    _order = 'id desc, name desc'
    name = fields.Char(string="Vendor Grade")


class ResPartner(models.Model):
    _inherit = ['res.partner']
    vendor_id = fields.Many2one('vendor.grade', string="Vendor Grade")


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']
    vendor_grade_id = fields.Many2one('vendor.grade', string="Vendor Grading")

    @api.model
    def create(self, vals):
        if 'partner_id' in vals:
            partner_id = vals.get("partner_id")
            if partner_id:
                browse_id = self.env['purchase.order'].browse(partner_id)
        return super(PurchaseOrder, self).create(vals)

    @api.onchange("partner_id")
    def set_value_to(self):
        self.vendor_grade_id = self.partner_id.vendor_id



