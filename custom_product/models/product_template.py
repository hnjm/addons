from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('name')
    def _check_name_product_template(self):
        for record in self:
            product_check = self.search([
                ('id', '!=', record.id),
                ('name', '=', record.name)
            ])
            if product_check:
                raise UserError(_("The name of product must be unique!"))
