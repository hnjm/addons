from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.sequence.abc') or _('New')
        return super(SaleOrder, self).create(vals)


