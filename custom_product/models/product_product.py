from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class ProductProduct(models.Model):
    _inherit = 'product.product'

    optional_product = fields.Many2many('product.product', 'product_product_optional', 'product_id',
                                        'optional_product_id', string='Optional Product')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context = self._context or {}
        if context.get('option_product'):
            domain = [
                ('id', '!=', context.get('product_id'))
            ]
            records = self.search(domain + args, limit=limit)
            return records.name_get()
        return super(ProductProduct, self).name_search(
            name, args, operator, limit)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        if context.get('option_product'):
            args += [('id', '!=', context.get('product_id'))]
        return super(ProductProduct, self).search(args, offset, limit, order, count=count)
