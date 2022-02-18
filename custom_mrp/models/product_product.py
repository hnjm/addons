from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_bom_price(self, bom, boms_to_recompute=False, byproduct_bom=False):
        total = super(ProductProduct, self)._compute_bom_price(bom, boms_to_recompute=False, byproduct_bom=False)
        for i in bom:
            for line in i.operation_ids:
                if line.workcenter_id.is_outsource:
                    total += line.price_cost
        return total