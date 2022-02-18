# -*- coding: utf-8 -*-

import json
from odoo import api, models, fields, _
from odoo.tools import float_round


class ReportBomStructure(models.AbstractModel):
    _inherit= 'report.mrp.report_bom_structure'

    def _get_operation_line(self, product, bom, qty, level):
        operations = []
        total = 0.0
        qty = bom.product_uom_id._compute_quantity(qty, bom.product_tmpl_id.uom_id)
        total_bom_cost = 0
        for operation in bom.operation_ids:
            if operation._skip_operation_line(product):
                continue
            operation_cycle = float_round(qty / operation.workcenter_id.capacity, precision_rounding=1, rounding_method='UP')
            duration_expected = operation_cycle * (operation.time_cycle + (operation.workcenter_id.time_stop + operation.workcenter_id.time_start))
            total = ((duration_expected / 60.0) * operation.workcenter_id.costs_hour)
            if operation.workcenter_id.is_outsource:
                total_bom_cost = operation.price_cost + total
                quantity = sum(i.product_qty for i in bom.bom_line_ids.filtered(lambda x: x.operation_id.id == operation.id))
                operations.append({
                    'level': level or 0,
                    'operation': operation,
                    'name': operation.name + ' - ' + operation.workcenter_id.name,
                    'duration_expected': duration_expected,
                    'total': total_bom_cost,
                    'product_cost': operation.price_cost or 0,
                    'quantity': quantity,
                    'bom': bom
                })
            else:
                operations.append({
                    'level': level or 0,
                    'operation': operation,
                    'name': operation.name + ' - ' + operation.workcenter_id.name,
                    'duration_expected': duration_expected,
                    'total': self.env.company.currency_id.round(total),
                    'product_cost': operation.price_cost or 0,
                    'quantity': 0,
                    'bom': bom
                })
        return operations

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        res = super(ReportBomStructure, self)._get_bom(bom_id, product_id, line_qty, line_id, level)
        operations = res['operations']
        print(operations)
        res['product_cost'] = sum([op['product_cost'] for op in operations])
        res['total_quantity'] = sum([op['quantity'] for op in operations])
        return res