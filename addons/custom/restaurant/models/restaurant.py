from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class RestStaff(models.Model):
    _name = 'rest.staff'
    _description = "This Model will be store data of our staff"
    _rec_name = "mobile"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string="Staff Name", track_visibility="always")
    age = fields.Integer(string="Age", track_visibility="always")
    dob = fields.Date(string="DOB")
    mobile = fields.Char(string="Mobile", size=10, track_visibility="always", required=True)
    email = fields.Char(string="Email", track_visibility="always")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])

    country_id = fields.Many2one('res.country', string='Country')
    country_code = fields.Char(string="Country Code", related="country_id.code")

    staff_line_ids = fields.One2many('rest.staff.lines', 'connecting_field', string="Staff Line")
    sequence = fields.Integer(string="Seq.")
    status = fields.Selection([('active', 'Active'), ('resigned', 'Resigned')], string="Status", readonly=True,
                              default="active")
    image = fields.Binary(string="Image")

    hand_salary = fields.Float(string="In Hand Salary")
    epf_esi = fields.Float(string="EPF+ESI")
    ctc_salary = fields.Float(string="CTC", compute="ctc_calc")

    seq_num = fields.Char(string='Seq No.', required=True, copy=False, index=True, readonly=True, default=lambda self: _('New'))

    button_integer = fields.Integer(string="Button Integer")

    @api.depends('hand_salary', 'epf_esi')
    def ctc_calc(self):
        for record in self:
            ctc = 0
            if record.hand_salary:
                ctc = ctc + record.hand_salary
            if record.epf_esi:
                ctc = ctc + record.epf_esi
            record.ctc_salary = ctc

    def new_fun(self):
        print("new function print")

    # Delete One2many field data
    def delete_one2many(self):
        for record in self:
            if record.staff_line_ids:
                record.staff_line_ids = [(5, 0, 0)]
                return {'effect': {
                    'fadeout': 'slow',
                    'type': 'rainbow_man',
                    'message': 'Record has been deleted successfully.'
                }}
            return {'effect': {
                'fadeout': 'slow',
                'type': 'rainbow_man',
                'message': 'Record Not Found'
            }}

    # check_orm button
    # def check_orm(self):
    #     search_var = self.env['rest.staff'].search([('gender', '=', 'male')])
    #     print("____Search____", search_var)
    #     for rec in search_var:
    #         print("_____Record______", rec.name, "_____Gender_____", rec.gender)

    @api.model
    def create(self, vals):
        if vals.get('seq_num', _('New')) == _('New'):
            vals['seq_num'] = self.env['ir.sequence'].next_by_code('rest.seq.staff') or _('New')
        res = super(RestStaff, self).create(vals)
        if vals.get('gender') == 'male':
            res['name'] = "Mr." + res['name']
        if vals.get('gender') == 'female':
            res['name'] = "Mrs." + res['name']
        return res

    # @api.model
    # def write(self, vals):
    #     if vals.get('seq_num', _('New')) == _('New'):
    #         vals['seq_num'] = self.env['ir.sequence'].next_by_code('rest.seq.staff') or _('New')
    #     res = super(RestStaff, self).write(vals)
    #     return res

    def do_resign(self):
        for rec in self:
            rec.status = 'resigned'

    @api.constrains('age', 'mobile')
    def val_age(self):
        for record in self:
            if record.age <= 18:
                raise ValidationError(_('The age must be greater than 18.'))
            if len(record.mobile) < 10:
                raise ValidationError(_('The mobile number must be equal to 10 digit'))


class RestStaffLine(models.Model):
    _name = 'rest.staff.lines'
    connecting_field = fields.Many2one('rest.staff', string="Staff ID")

    name = fields.Char(string='Name', required=True)
    product_id = fields.Many2one('product.product', string="Product")
    sequence = fields.Integer(string="Seq.")
