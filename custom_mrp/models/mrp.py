from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class MRP(models.Model):
    _inherit = 'mrp.production'

    sequence_mrp = fields.Integer('stt')
    mrp_ref = fields.Char('Ref')
    old_name = fields.Char('Old Name')

    def action_confirm(self, is_outsource=False):
        self._check_company()
        for production in self:
            if production.bom_id:
                production.consumption = production.bom_id.consumption
            # In case of Serial number tracking, force the UoM to the UoM of product
            if production.product_tracking == 'serial' and production.product_uom_id != production.product_id.uom_id:
                production.write({
                    'product_qty': production.product_uom_id._compute_quantity(production.product_qty, production.product_id.uom_id),
                    'product_uom_id': production.product_id.uom_id
                })
                for move_finish in production.move_finished_ids.filtered(lambda m: m.product_id == production.product_id):
                    move_finish.write({
                        'product_uom_qty': move_finish.product_uom._compute_quantity(move_finish.product_uom_qty, move_finish.product_id.uom_id),
                        'product_uom': move_finish.product_id.uom_id
                    })
            if not is_outsource:
                production.move_raw_ids._adjust_procure_method()
            if is_outsource:
                production.move_raw_ids._adjust_procure_method(is_outsource=True)
            (production.move_raw_ids | production.move_finished_ids)._action_confirm(merge=False)
            production.workorder_ids._action_confirm()
        # run scheduler for moves forecasted to not have enough in stock
        self.move_raw_ids._trigger_scheduler()
        self.picking_ids.filtered(
            lambda p: p.state not in ['cancel', 'done']).action_confirm()
        # Force confirm state only for draft production not for more advanced state like
        # 'progress' (in case of backorders with some qty_producing)
        self.filtered(lambda mo: mo.state == 'draft').state = 'confirmed'
        return True