from odoo import fields, models, api, _
from odoo import http
from cuttpy import Cuttpy
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

# API_KEY = "c74bb2d34c35120f311aa7b4f110cc196f718517"
# connection = bitly_api.Connection(access_token=API_KEY)

class ApiKey:

    def apikey(self, ids, main_url):
        api_id = ids.api_key
        if api_id:
            try:
                shortner = Cuttpy(f"{api_id}")
                url = shortner.shorten(f"{main_url}")
                _logger.debug('validated data')
                return url.shortened_url
            except Exception as e:
                _logger.debug('validated data', e)
                return main_url
        else:
            ValidationError(
                _('Api Key not found, please store your cuttly api key.'))

            # try:
            #     shortner = Cuttpy(f"{api_id}")
            #     url = shortner.shorten(f"{main_url}")
            #     return url.shortened_url
            # except:
            #     return main_url


class StockPicking(models.Model):
    _inherit = ['stock.picking']

    @api.model
    def stocklocationurl(self, location_id):
        host = http.request.env['ir.config_parameter'].get_param('web.base.url')  # BASE URL
        action_id = self.env.ref("stock.location_open_quants")
        ids = self.env['res.config.settings'].search([])
        # main_url = f"{host}/web#cids=1&menu_id=108&action={action_id.id}&active_id={location_id}&model=stock.quant&view_type=list"
        main_url = f"https://mailtrap.io/inboxes/1885525/messages/3011055403"
        url = ApiKey().apikey(ids, main_url)
        return url

        # if self.id:
        #     # main_url = f"{host}/web#cids=1&menu_id=108&action={action_id.id}&active_id={location_id}&model=stock.quant&view_type=list"
        #     # main_url = f"https://www.google.com/"
        #     try:
        #         # connection = bitly_api.Connection(access_token=api_id[0])
        #         # dict_url = connection.shorten(uri=main_url)
        #         # url = dict_url.get('url')
        #         # return url
        #         pass
        #     except:
        #         url = main_url
        #         return url


class ProductTemplate(models.AbstractModel):
    _inherit = ['product.template']

    @api.model
    def producturl(self, o):
        host = http.request.env['ir.config_parameter'].get_param('web.base.url')  # BASE URL
        action_id = self.env.ref("stock.product_template_action_product")
        menu_id = self.env.ref("base.grant_menu_access")
        ids = self.env['res.config.settings'].search([])
        main_url = f"https://pypi.org/project/cuttpy/"
        # main_url = f"{host}/web#id={o}&cids=1&menu_id={menu_id.id}&action={action_id.id}&model=product.template&view_type=form"
        url = ApiKey().apikey(ids, main_url)
        print(url)
        return url
        # api_id = [i.api_key for i in ids if i.api_key]
        # if o:
        #     # main_url = f"{host}/web#id={o}&cids=1&menu_id={menu_id.id}&action={action_id.id}&model=product.template&view_type=form"
        #     main_url = f"https://www.google.com/"
        #     try:
        #         connection = bitly_api.Connection(access_token=api_id[0])
        #         dict_url = connection.shorten(uri=main_url)
        #         url = dict_url.get('url')
        #         return url
        #     except:
        #         url = main_url
        #         return url
