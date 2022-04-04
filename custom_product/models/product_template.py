from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    customer_reference = fields.Char(string='Customer Reference')
    fast_accounting_no = fields.Char(string='FAST accounting No.')
    revision = fields.Char(string='Revision')
    material = fields.Char(string='Material')

    @api.constrains('name')
    def _check_name_product_template(self):
        for record in self:
            product_check = self.search([
                ('id', '!=', record.id),
                ('name', '=', record.name)
            ])
            if product_check:
                raise UserError(_("The name of product must be unique!"))

    @api.model
    def _cron_update_customer_reference(self):
        for record in self.env['product.template'].search([]):
            # record.customer_reference = record.default_code
            record.default_code = record.x_studio_drawing_number
