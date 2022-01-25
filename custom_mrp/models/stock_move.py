from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _subcontracted_produce(self, subcontract_details, is_outsource=False):
        self.ensure_one()
        for move, bom in subcontract_details:
            mo = self.env['mrp.production'].with_company(move.company_id).create(
                self._prepare_subcontract_mo_vals(move, bom))
            a = self.env['stock.move'].create(mo._get_moves_raw_values())
            b = self.env['stock.move'].create(mo._get_moves_finished_values())
            mo.date_planned_finished = move.date
            # Avoid to have the picking late depending of the MO
            if not is_outsource:
                mo.action_confirm()
            if is_outsource:
                mo.action_confirm(is_outsource=True)

            # Link the finished to the receipt move.
            finished_move = mo.move_finished_ids.filtered(lambda m: m.product_id == move.product_id)
            finished_move.write({'move_dest_ids': [(4, move.id, False)]})
            mo.action_assign()


class StockMove(models.Model):
    _inherit = 'stock.move'


    def _adjust_procure_method(self, is_outsource=False):
        """ This method will try to apply the procure method MTO on some moves if
        a compatible MTO route is found. Else the procure method will be set to MTS
        """
        # Prepare the MTSO variables. They are needed since MTSO moves are handled separately.
        # We need 2 dicts:
        # - needed quantity per location per product
        # - forecasted quantity per location per product
        mtso_products_by_locations = defaultdict(list)
        mtso_needed_qties_by_loc = defaultdict(dict)
        mtso_free_qties_by_loc = {}
        mtso_moves = self.env['stock.move']

        for move in self:
            product_id = move.product_id
            domain = [
                ('location_src_id', '=', move.location_id.id),
                ('location_id', '=', move.location_dest_id.id),
                ('action', '!=', 'push')
            ]
            rules = self.env['procurement.group']._search_rule(False, move.product_packaging_id, product_id, move.warehouse_id, domain)

            if rules:
                if rules.procure_method in ['make_to_order', 'make_to_stock']:
                    move.procure_method = rules.procure_method
                else:
                    # Get the needed quantity for the `mts_else_mto` moves.
                    mtso_needed_qties_by_loc[rules.location_src_id].setdefault(product_id.id, 0)
                    mtso_needed_qties_by_loc[rules.location_src_id][product_id.id] += move.product_qty

                    # This allow us to get the forecasted quantity in batch later on
                    mtso_products_by_locations[rules.location_src_id].append(product_id.id)
                    mtso_moves |= move
            else:
                if is_outsource:
                    move.procure_method = 'make_to_order'
                else:
                    move.procure_method = 'make_to_stock'

        # Get the forecasted quantity for the `mts_else_mto` moves.
        for location, product_ids in mtso_products_by_locations.items():
            products = self.env['product.product'].browse(product_ids).with_context(location=location.id)
            mtso_free_qties_by_loc[location] = {product.id: product.free_qty for product in products}

        # Now that we have the needed and forecasted quantity per location and per product, we can
        # choose whether the mtso_moves need to be MTO or MTS.
        for move in mtso_moves:
            needed_qty = move.product_qty
            forecasted_qty = mtso_free_qties_by_loc[move.location_id][move.product_id.id]
            if float_compare(needed_qty, forecasted_qty, precision_rounding=product_id.uom_id.rounding) <= 0:
                move.procure_method = 'make_to_stock'
                mtso_free_qties_by_loc[move.location_id][move.product_id.id] -= needed_qty
            else:
                move.procure_method = 'make_to_order'