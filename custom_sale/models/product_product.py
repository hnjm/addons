from odoo import api, models, fields, _


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _rec_name = "default_code"


class ProductProduct(models.Model):
    _inherit = "product.product"
    _rec_name = "default_code"

    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'default_code'])
        return [(template.id, '%s' % (template.default_code or '')) for template in self]
