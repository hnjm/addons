from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict
import re


class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    is_created_purchase = fields.Boolean(string="Is Created Purchase")

    def button_start(self):
        res = super(WorkOrder, self).button_start()
        subcontract_details_per_picking = defaultdict(list)
        for record in self:
            if record.workcenter_id.is_outsource and record.is_created_purchase is False:
                operation_line = record.production_id.bom_id.operation_ids.filtered(lambda x: x.workcenter_id.id == record.workcenter_id.id)
                val_po = {}
                if operation_line:
                    if operation_line[0].partner_id:
                        val_po = {
                            'partner_id': operation_line[0].partner_id.id
                        }
                    else:
                        raise UserError(_("Please choose Vendor for Operation in BOM"))
                else:
                    raise UserError(_("Please add more Operation Line for BOM"))
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
                            'product_uom_id': line.product_id.uom_id.id,
                            'location_id': i.location_id.id or False,
                            'location_dest_id': i.location_dest_id.id or False,
                            'move_id': line.id,
                            'picking_id': i.id
                        }
                        self.env['stock.move.line'].create(value)
                # YC5 ref. https://docs.google.com/spreadsheets/d/1WXF4D6uA0AdY3hQREy7elj_XA7M25Rc30OBlNWtmFyM/edit#gid=329401541
                partner_id = operation_line[0].partner_id
                if record.workcenter_id and record.workcenter_id.product_id and operation_line and partner_id:
                    exist_po_line = self.env['purchase.order.line'].sudo().search([
                        ('product_id', '=', record.workcenter_id.product_id.id),
                        ('order_id.state', '=', 'draft'),
                        ('order_id.partner_id.id', '=', partner_id.id),
                    ], limit=1)
                    name = f"{record.workcenter_id.product_id.name} {re.sub(r'<.*?>', '', operation_line[0].note) or ''}"
                    if exist_po_line:
                        qty = exist_po_line.product_qty
                        new_origin = f'{exist_po_line.order_id.origin}, {record.production_id.name}' \
                            if exist_po_line.order_id.origin else record.production_id.name
                        # update
                        exist_po_line.product_qty = qty + (record.production_id.product_qty if record.production_id else 1)
                        exist_po_line.order_id.origin = new_origin
                        exist_po_line.name = name
                    else:
                        vals = {
                            'origin': record.production_id.name,
                            'partner_id': partner_id.id,
                            'order_line': [(0, 0, {
                                'name': name,
                                'product_id': record.workcenter_id.product_id.id,
                                'product_uom_qty': record.production_id.product_qty if record.production_id else 1,
                                'price_unit': operation_line[0].price_cost or 0,
                            })]
                        }
                        self.env['purchase.order'].create(vals)
                record.is_created_purchase = True

        return res

