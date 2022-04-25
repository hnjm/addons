# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError
import odoo.addons.decimal_precision as dp
import base64, zipfile, os
from io import BytesIO
from odoo.tools.osutil import tempdir

MAX_FILE_SIZE = 100 * 1024 * 1024  # in megabytes


class ProductImportImageWizard(models.TransientModel):
    _name = 'product.import.image.wizard'
    _description = u'Product Import Image'

    file = fields.Binary(u'Zip File', required=True)
    product_model = fields.Selection([('1', 'Product Template'), ('2', 'Product Variants')], string="Product Model")
    pdt_operation = fields.Selection([('1', 'Product Creation'), ('2', 'Product Updation')], string="Product Operation")
   
    def button_import(self):
        self.ensure_one()
        zip_data = base64.decodestring(self.file)
        fp = BytesIO()
        fp.write(zip_data)
    
        if not fp:
            raise Exception(_("No file sent."))
        if not zipfile.is_zipfile(fp):
            raise UserError(_('Only zip files are supported.'))

        with zipfile.ZipFile(fp, "r") as z:
            for zf in z.filelist:
                if zf.file_size > MAX_FILE_SIZE:
                    raise UserError(_("File '%s' exceed maximum allowed file size") % zf.filename)

                (name, extension) = os.path.splitext(zf.filename)
                product_obj = self.env['product.product']
                if self.product_model == '1':
                    product_obj = self.env['product.template']
                data = z.read(zf.filename)
                vals = {
                        'name':name,
                        'image_1920':base64.b64encode(data)
                    }
                product_id = product_obj.search(
                    ['|','|',('name','=',name),('default_code', '=', name), ('barcode', '=', name)],limit=1)

                if self.pdt_operation == '1' and not product_id:
                    product_obj.create(vals)
                elif self.pdt_operation == '1' and product_id:
                    product_id.write(vals)
                elif self.pdt_operation == '2' and product_id:
                    product_id.write(vals)
                elif not product_id and self.pdt_operation == '2':
                    raise UserError("Could not find the product '%s'" % name)
        
