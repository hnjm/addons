from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    def button_start(self):
        res = super(WorkOrder, self).button_start()
        subcontract_details_per_picking = defaultdict(list)
        for record in self:
            if record.workcenter_id.is_outsource and record.workcenter_id.partner_id:
                val_po = {
                    'partner_id': record.workcenter_id.partner_id.id
                }
                purchase = self.env['purchase.order'].create(val_po)
                value_po_line = {
                    'product_id': record.product_id.id,
                    'product_qty': 1,
                    'order_id': purchase.id
                }
                purchase_order_line = self.env['purchase.order.line'].create(value_po_line)
                purchase.button_confirm()
                picking_ids = purchase.picking_ids[0]
                bom = self.env['mrp.bom'].sudo().search([
                        ('product_tmpl_id', '=', record.product_id.product_tmpl_id.id)
                    ], limit=1)
                move = self.env['stock.move'].search([
                    ('purchase_line_id', '=', purchase_order_line.id)
                ])
                move.write({
                    'is_subcontract': True,
                    'location_id': move.picking_id.partner_id.with_company(
                        move.company_id).property_stock_subcontractor.id
                })
                subcontract_details_per_picking[move.picking_id].append((move, bom))
                for picking, subcontract_details in subcontract_details_per_picking.items():
                    picking._subcontracted_produce(subcontract_details, is_outsource=True)
                mo = self.env['mrp.production'].search([
                    ('procurement_group_id.name', '=', picking_ids.name)
                ])
                picking_mo = mo.picking_ids
                for i in picking_mo:
                    for line in i.move_ids_without_package:
                        value = {
                            'product_id': line.product_id.id,
                            'location_id': i.location_id.id or False,
                            'location_dest_id': i.location_dest_id.id or False,
                            'move_id': line.id,
                            'picking_id': i.id
                        }
                        self.env['stock.move.line'].create(value)
        return res