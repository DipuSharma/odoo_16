from odoo import fields, models, api


class SkuCategory(models.Model):
    _name = "sku.categories"
    _description = "This model use for sku category."

    name = fields.Char(string="Category Name")
    sku = fields.Char(string="Sku")

    @api.onchange('name')
    def set_sku(self):
        sku_list = []
        if self.name:
            if len(self.name) < 4:
                sku_list.append(self.name)
        self.sku = ''.join(sku_list)


class SkuType(models.Model):
    _name = "sku.types"
    _description = "This model use for sku type"

    name = fields.Char(string="Product Type")
    sku = fields.Char(string="Sku")
    variable = fields.Char(string="Variable")
    category_id = fields.Many2one('sku.categories', string="Category Name")


class SkuColorShape(models.Model):
    _name = "sku.shapes"
    _description = "This model use for sku color and shape"

    name = fields.Char(string="Shape/Color/Desc")
    sku = fields.Char(string="Sku")


class SkuBonded(models.Model):
    _name = "sku.bondedes"
    _description = "This model use for sku bonded"

    name = fields.Char(string="Secondry/Bonded")
    sku = fields.Char(string="Sku")
    variable = fields.Char(string="Variable")


class SkuVendor(models.Model):
    _name = "sku.vendores"
    _description = "This model use for sku vendor"

    name = fields.Char(string="Vendor")
    sku = fields.Char(string="Sku")


class SkuCountryOrigin(models.Model):
    _name = "sku.countries"
    _description = "This model use for sku country of origin"

    name = fields.Char(string="Country")
    sku = fields.Char(string="Sku")


class SkuVolumeDescription(models.Model):
    _name = "sku.volumes"
    _description = "This model use for sku volume and descriptions"

    name = fields.Char(string="Volume Description")
    sku = fields.Char(string="Sku")


class ProductTemplate(models.Model):
    _inherit = ['product.template', ]

    productcategorysku_id = fields.Many2one(
        'sku.categories', string="Product Category", help="Enter Category")
    producttypesku_id = fields.Many2one(
        'sku.types', string='Product Type', help="Enter Type", domain="[('category_id', '=', productcategorysku_id)]")
    sbondedsku_id = fields.Many2one(
        'sku.bondedes', string="Secondary Stone", help="Enter Bonded")
    shapesku1_id = fields.Many2one(
        'sku.shapes', string="Shape/Color/Desc", help="Enter Shape/Color")
    countrysku_id = fields.Many2one(
        'sku.countries', string="Country of Origin", help="Enter Country")
    shapesku2_id = fields.Many2one(
        'sku.shapes', string="Shape/Color/Desc", help="Enter Shape/Color")
    vendorsku_id = fields.Many2one(
        'sku.vendores', string="Vendor", help="Enter Vender")
    volumesku_id = fields.Many2one(
        'sku.volumes', string="Volume Size", help="Enter Volume")
    sku_code = fields.Char(string="Sku", help="Generated sku")

    @api.onchange('productcategorysku_id', 'producttypesku_id', 'vendorsku_id', 'sbondedsku_id', 'shapesku1_id',
                  'countrysku_id', 'shapesku2_id', 'volumesku_id')
    def _get_func(self):

        if self.productcategorysku_id or self.producttypesku_id or self.shapesku1_id or self.sbondedsku_id or \
                self.vendorsku_id or self.countrysku_id or self.shapesku2_id or self.volumesku_id:
            s_category = self.productcategorysku_id.sku
            s_type = self.producttypesku_id.sku
            s_type_variable = self.producttypesku_id.variable
            s_shapes1 = self.shapesku1_id.sku
            s_shapes2 = self.shapesku2_id.sku
            s_bonded = self.sbondedsku_id.sku
            s_bonded_variable = self.sbondedsku_id.variable
            s_vendor = self.vendorsku_id.sku
            s_volumes = self.volumesku_id.sku
            s_country = self.countrysku_id.sku

            arry_sku_code = []
            if s_category:
                arry_sku_code.append(s_category)
            if s_type:
                arry_sku_code.append(s_type)
            if s_type_variable:
                arry_sku_code.append(s_type_variable)
            if s_shapes1:
                arry_sku_code.append(s_shapes1)
            if s_bonded:
                arry_sku_code.append(s_bonded)
            if s_bonded_variable:
                arry_sku_code.append(s_bonded_variable)
            if s_shapes2:
                arry_sku_code.append(s_shapes2)
            if s_vendor and not s_country:
                arry_sku_code.append(s_vendor)
            if s_vendor and s_country:
                combine_data = f"{s_vendor}{s_country}"
                arry_sku_code.append(combine_data)
            if s_country and not s_vendor:
                arry_sku_code.append(s_country)
            if s_volumes:
                arry_sku_code.append(s_volumes)

            self.sku_code = '-'.join(arry_sku_code)

    @api.onchange('productcategorysku_id')
    def set_values_to(self):
        self.producttypesku_id = []
        res = {'domain': {'producttypesku_id': []}}
        if self.productcategorysku_id:
            res['domain']['producttypesku_id'] = [('category_id', '=', self.productcategorysku_id.id)]
        return res
