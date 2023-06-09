try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
# from barcode import EAN13
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError
# from barcode.writer import ImageWriter


class Product(models.Model):
    """ inherit Invoice to add report settings """
    _inherit = "product.template"
    qr_code = fields.Binary('QRcode', compute="_generate_qr")
    # bar_code = fields.Binary('Barcode', compute="_generate_bar_code")

    def _generate_qr(self):
        """method to generate QR code"""
        for rec in self:
            if qrcode and base64:

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                if rec.name:
                    qr.add_data("Product : ")
                    qr.add_data(rec.name)
                if rec.default_code:
                    qr.add_data(", Reference : ")
                    qr.add_data(rec.default_code)
                if rec.list_price:
                    qr.add_data(", Price : ")
                    qr.add_data(rec.list_price)
                qr.add_data(", Quantity : ")
                qr.add_data(rec.qty_available)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
            else:
                raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))

    # def _generate_bar_code(self):
    #     for rec in self:
    #         # Make sure to pass the number as string
    #         number = rec.default_code
    #
    #         # Now, let's create an object of EAN13 class and
    #         # pass the number with the ImageWriter() as the
    #         # writer
    #         my_code = EAN13(number, writer=ImageWriter())
    #
    #         # Our barcode is ready. Let's save it.
    #         my_code.save("new_code1")
