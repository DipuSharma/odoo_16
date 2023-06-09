from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class LogisticService(models.Model):
    _name = "logistic.service"
    _description = "This model use for logistic services"

    name = fields.Char(string="Logistic Service")


class ShipmentType(models.Model):
    _name = "shipment.type"

    name = fields.Char(string="Shipment Tracking Type")


class ShipmentTrack(models.Model):
    _name = "shipment.track"
    _description = "This model use for shipment tracking."
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Shipment Tracking', required=True, copy=False, index=True,
                       readonly=True, default=lambda self: _('New'))
    priority = fields.Selection([('0', 'Normal'), ('1', 'Important')], string='Sequence', readonly=False,
                                track_visibility="always",
                                states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    logistic_service = fields.Many2one('logistic.service', string="Logistic Service", readonly=False,
                                       tracking=True,
                                       states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    tracking_number = fields.Char(string="Tracking Number", readonly=False, tracking=True,
                                  states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    url_link = fields.Char(string="Link")
    shipment_type_id = fields.Many2one('shipment.type', string="Type of Shipping", readonly=False,
                                       tracking=True,
                                       states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    depart_date = fields.Date(string="Depart Date", readonly=False, tracking=True,
                              states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    eta = fields.Date(string="Estimate Arrival Date", tracking=True, readonly=False,
                      required=True, states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    internal_eta = fields.Date(string="SG ETA", tracking=True, readonly=False,
                               states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    cargo_spaces = fields.Char(string="Cargo Spaces", tracking=True, readonly=False,
                               states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})
    product_manager = fields.Many2one('res.users', string="Product Manager", tracking=True)
    vendor_cantact = fields.Many2one('res.users', string="Vendor Contact", tracking=True)
    sg_track_location = fields.Selection([('domestic', 'Domestic'), ('international', 'International')],
                                         string='Location')
    vendor_id = fields.Many2one('res.partner', 'Vendor', domain="[('is_company','=',False)]")
    state = fields.Selection(
        [('draft', 'Draft'), ('in_process', 'In Process'), ('receive', 'Shipment Delivered'), ('cancel', 'Cancelled')],
        tracking=True, string="Status", readonly=True, default="draft")
    shipment_line_id = fields.One2many('shipment.track.line', 'shipment_id', string="Related Purchase Orders",
                                       readonly=False,
                                       states={'receive': [('readonly', True)], 'cancel': [('readonly', True)]})

    def find_url(self, vals):
        weblink = None
        if vals.get('logistic_service') == 2 or self.logistic_service.id == 2:
            if vals.get('tracking_number'):
                weblink = f"http://www.dhl.com/content/g0/en/express/tracking.shtml?brand=DHL&AWB={vals.get('tracking_number')}"
            else:
                weblink = f"http://www.dhl.com/content/g0/en/express/tracking.shtml?brand=DHL&AWB={self.tracking_number}"
        if vals.get('logistic_service') == 7 or self.logistic_service.id == 7:
            if vals.get('tracking_number'):
                weblink = f"http://wwwapps.ups.com/WebTracking/processRequest?HTMLVersion=5.0&Requester=NES" \
                          f"&AgreeToTermsAndConditions=yes&loc=en_US&tracknum={vals.get('tracking_number')}"
            else:
                weblink = f"http://wwwapps.ups.com/WebTracking/processRequest?HTMLVersion=5.0&Requester=NES" \
                          f"&AgreeToTermsAndConditions=yes&loc=en_US&tracknum={self.tracking_number}"
        if vals.get('logistic_service') == 16 or self.logistic_service.id == 16:
            if vals.get('tracking_number'):
                weblink = f"https://www.fedex.com/fedextrack/?action=track&trackingnumber={vals.get('tracking_number')}"
            else:
                weblink = f"https://www.fedex.com/fedextrack/?action=track&trackingnumber={self.tracking_number}"
        return weblink

    def entery_data_edit_data(self, vals):
        purchaseID_list_arr = []
        state_list_arr = []
        shipment_line = []
        for record in vals.get('shipment_line_id'):
            if record[0] == 0:
                _pid = record[2].get('po_id')
                _state = record[2].get('state')
                if _pid in purchaseID_list_arr:
                    position = purchaseID_list_arr.index(_pid)
                    if _state != state_list_arr[position]:
                        raise ValidationError("Same PO can't be added having both partial and all items")
                else:
                    purchaseID_list_arr.append(_pid)
                    state_list_arr.append(_state)
                if record[2].get('state') == '0' and record[2].get('purchase_line_id') is None:
                    search_var = self.env['purchase.order.line'].search(
                        [('order_id', '=', record[2].get('po_id'))])
                    for var in search_var:
                        get_data = self.env['shipment.track.line'].search([('purchase_line_id', '=', var.id)])
                        if get_data:
                            raise ValidationError(
                                _(f"This PO, Item is already in another shipment #{get_data.shipment_id.name}."))
                        line = (0, record[1], {'po_id': record[2].get('po_id'), 'state': record[2].get('state'),
                                               'purchase_line_id': var.id, 'quantity': var.product_qty})
                        shipment_line.append(line)
                if record[2].get('state') == '1' and record[2].get('purchase_line_id') is not None:
                    particular_line = (
                        0, record[1], {'po_id': record[2].get('po_id'), 'state': record[2].get('state'),
                                       'purchase_line_id': record[2].get('purchase_line_id'),
                                       'quantity': record[2].get('quantity')})
                    shipment_line.append(particular_line)
            if record[0] == 1:
                if not record[2].get('purchase_line_id') or not record[2].get('state'):
                    pre_line = (record[0], record[1], {'state': None, 'purchase_line_id': None, 'quantity': 0.0})
                    shipment_line.append(pre_line)
                if record[2].get('state'):
                    pre_line = (record[0], record[1], {'state': record[2].get('state')})
                    shipment_line.append(pre_line)
                if record[2].get('purchase_line_id'):
                    add_line_data = (record[0], record[1], {'purchase_line_id': record[2].get('purchase_line_id'), 'quantity': record[2].get('quantity')})
                    shipment_line.append(add_line_data)
            if record[0] == 2:
                remove_data = (record[0], record[1], 0)
                shipment_line.append(remove_data)
            if record[0] == 4:
                exist_data = (record[0], record[1], 0)
                shipment_line.append(exist_data)
        return shipment_line

    @api.model
    def create(self, vals):
        get_link = ShipmentTrack.find_url(self, vals)
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('shipment.track.sequence') or _('New')
        vals['url_link'] = get_link
        if vals.get('shipment_line_id'):
            shipment_track_line_list = ShipmentTrack.entery_data_edit_data(self, vals)
            vals['shipment_line_id'] = shipment_track_line_list
        if self.shipment_line_id:
            pass
        res = super(ShipmentTrack, self).create(vals)
        return res

    def write(self, vals):
        get_link = ShipmentTrack.find_url(self, vals)
        vals['url_link'] = get_link
        if vals.get('shipment_line_id'):
            shipment_track_line_list = ShipmentTrack.entery_data_edit_data(self, vals)
            vals['shipment_line_id'] = shipment_track_line_list
        res = super(ShipmentTrack, self).write(vals)
        return res

    def confirm_tracking(self):
        for rec in self:
            if not rec.shipment_line_id:
                raise ValidationError(_("Unable to confirm tracking, PO items must be added."))
            for data in rec.shipment_line_id.purchase_line_id:
                if not data.id:
                    raise ValidationError(_("Unable to confirm tracking, PO product item must be added."))
            rec.state = 'in_process'

    def do_cancel(self):
        self.write({'state': 'cancel'})

    def received(self):
        for rec in self:
            if not rec.shipment_line_id:
                raise ValidationError(_("Unable to mark shipment as received, PO items must be added."))
            rec.state = 'receive'

    def set_draft(self):
        for rec in self:
            get_shipment_line_list = self.env['shipment.track.line'].search([('shipment_id', '=', rec.id)])
            if len(get_shipment_line_list) > 1:
                raise ValidationError(_("With another shipment tracking same product under process."))
            else:
                rec.state = 'draft'

    def action_url(self):
        for rec in self:
            if not self.url_link:
                raise ValidationError(_("Track url not found please choose logistic service, add tracking number or "
                                        "this service is not currently supported."))
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': rec.url_link
            }

    @api.onchange('eta')
    def check_date(self):
        if self.eta or self.depart_date:
            d_date = self.depart_date
            e_date = self.eta
            if d_date > e_date:
                raise ValidationError(_('The Estimate arrival date not lower than Depart date.'))

    def copy(self, default=None):
        if self.state == 'cancel':
            raise ValidationError(_('This Shipment Order is Cancelled, So its not copy.'))
        ctx = dict(self.env.context)
        ctx.pop('default_product_id', None)
        duplicate = self.with_context(ctx)
        copy_shipment = super(ShipmentTrack, self).copy(default=default)
        return copy_shipment

    @api.ondelete(at_uninstall=False)
    def _unlink_if_cancelled(self):
        for order in self:
            if not order.state == 'cancel':
                raise UserError(_('In Shipment track to delete, you must cancel it first.'))

    @api.constrains('shipment_line_id')
    def _check_exist_product_in_line(self):
        for record in self:
            exist_product_list = []
            for line in record.shipment_line_id:
                if line.purchase_line_id.id in exist_product_list:
                    raise ValidationError(_('Product should be one per line.'))
                exist_product_list.append(line.purchase_line_id.id)


class ShipmentTrackLine(models.Model):
    _name = 'shipment.track.line'
    shipment_id = fields.Many2one('shipment.track', string="Ship Tracking ID", ondelete='cascade')
    po_id = fields.Many2one('purchase.order', string="PO#", ondelete='cascade')
    state = fields.Selection([('0', 'All Item'), ('1', 'Partial Item')], string="Partial/All Item")
    purchase_line_id = fields.Many2one('purchase.order.line', string="Product", ondelete='cascade',
                                       domain="[('order_id', '=', po_id)]", states={'0': [('readonly', True)]})
    quantity = fields.Char(string="Quantity", ondelete='cascade')

    @api.onchange("purchase_line_id")
    def set_value_to(self):
        for rec in self:
            search_var = self.env['shipment.track.line'].search([('purchase_line_id', '=', rec.purchase_line_id.id)])
            for data in search_var.shipment_id:
                if search_var.purchase_line_id.id and 'cancel' not in data.state:
                    raise ValidationError(
                        _(f"This item is already in another shipment #{data.name}."))
            rec.quantity = self.purchase_line_id.product_qty


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = ['purchase.order.line']

    shipment_id = fields.Many2one('shipment.track', string="Shipment Order", ondelete='cascade',
                                  compute='automate')
    shipment_status = fields.Char(string="Shipment Status")

    @api.onchange("product_id")
    def automate(self):
        self.shipment_id = []
        for record in self:
            search_var = self.env['shipment.track.line'].search([('purchase_line_id', '=', record.id)])
            for data in search_var.shipment_id:
                if not data:
                    record.shipment_id = None
                    record.shipment_status = None
                if data.state == 'cancel':
                    record.shipment_id = None
                    record.shipment_status = data.state.upper()
                else:
                    record.shipment_id = data.id
                    record.shipment_status = data.state.upper()

    @api.onchange("shipment_ids")
    def set_value_to(self):
        for rec in self:
            rec.shipment_status = rec.shipment_ids.state


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ['purchase.order']

    shipment_line = fields.One2many('shipment.fetch.line', 'track_field', string="Related Purchase Orders",
                                    readonly=False)
    shipment_track_enabled = fields.Char(string="Shipment Enabled", compute="add_default_data", default="True")

    def add_default_data(self):
        if self.id:
            search_var = self.env['shipment.track.line'].search([('po_id', '=', self.id)])
            filtered = [i for i in search_var.shipment_id if i.id == i.id]
            purchase_opj = self.env['shipment.fetch.line']
            default = [(5, 0, 0)]
            if len(filtered) == 0:
                self.shipment_line = default
            if len(filtered) > 0:
                self.shipment_line = default
                for rec in range(len(filtered)):
                    purchase_opj.create(
                        {'shipment_ids': filtered[rec].id, 'shipment_status': filtered[rec].state,
                         'track_field': self.id})
        self.shipment_track_enabled = "True"


class ShipmentFetchLine(models.Model):
    _name = "shipment.fetch.line"

    track_field = fields.Many2one('purchase.order', ondelete='cascade')
    number_track = fields.Char(String="S.No", readonly=True)
    shipment_ids = fields.Many2one('shipment.track', string="Shipment Tracking", ondelete='cascade', readonly=True)
    shipment_status = fields.Char(string="Status", compute="automate", ondelete='cascade')

    def automate(self):
        self.shipment_status = None
        for record in self:
            search_var = self.env['shipment.track'].search([('id', '=', record.shipment_ids.id)])
            if record.shipment_ids.id == search_var.id:
                record.shipment_status = search_var.state

    @api.onchange("shipment_ids")
    def set_value_to(self):
        for rec in self:
            rec.shipment_status = rec.shipment_ids.state
