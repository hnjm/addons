#-*- coding: utf-8 -*-
from odoo import models, fields, api, tools,SUPERUSER_ID,_
from odoo.tools import float_round
from odoo.exceptions import UserError

class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'
    

    def _groupby_move_raw_temp_product(self,product_id):
        results = {}
        for raw in self.move_raw_ids.filtered(lambda x:x.product_id.id==product_id.id):
            key = (raw.product_id.product_tmpl_id.categ_id.id,raw.product_id.id)
            if not key in results:
                results[key] = self.env['stock.move']
            results[key] += raw
        return results

    @api.onchange('qty_producing')
    def _onchange_qty_producing(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        if self.qty_producing>0:
            miss_pack_msg=[]
            product_bom=self.bom_id.bom_line_ids.mapped('product_id').ids
            if (len(product_bom)==0 and len(product_bom)>0) and len(self.move_raw_ids)>0:
                raise UserError(_('Not enough components!.'))
            if self.state=='done':
                if self.qty_producing>self.qty_produced:
                   raise UserError(_('The production quantity should not be greater than the quantity produced.!.')) 
            for bom_line_id in self.bom_id.bom_line_ids:
                groups_raw = self._groupby_move_raw_temp_product(bom_line_id.product_id).values() 
                reserved_availability = 0.0
                quantity_done = 0.0
                should_consume_qty = 0.0
                avail_qty_uom=0.0
                should_consume_qty_uom=0.0
                product_uom_qty=0.0
                for data in groups_raw:
                    should_consume_qty += data.should_consume_qty
                    reserved_availability += data.reserved_availability 
                    quantity_done += data.quantity_done 
                    product_uom_qty+=data.product_uom_qty   
                
                should_consume_qty_uom=float_round(should_consume_qty,precision_digits=precision)
                avail_qty_uom = float_round(reserved_availability,precision_digits=precision) if self.state!='done' else float_round(product_uom_qty,precision_digits=precision)
                miss_qty=float_round(should_consume_qty_uom - avail_qty_uom,precision_digits=precision) 
                if avail_qty_uom<0:
                    miss_pack_msg.append(_(
                        '%s (%s) : Qty needed use (%s) - Available Qty (%s) => Missing Qty (%s) . \n') % (
                                    bom_line_id.product_id.display_name, bom_line_id.product_id.uom_id.name, abs(should_consume_qty_uom), abs(avail_qty_uom), abs(avail_qty_uom)))
                elif float(should_consume_qty_uom - avail_qty_uom) > 0:
                    miss_pack_msg.append(_(
                        '%s (%s) : Qty needed use (%s) - Available Qty (%s) => Missing Qty (%s) . \n') % (
                                    bom_line_id.product_id.display_name, bom_line_id.product_id.uom_id.name, abs(should_consume_qty_uom), abs(avail_qty_uom), abs(miss_qty)))
            if len(miss_pack_msg)>0:
                raise UserError(_('(*) Materials used are not enough:\n\n %s')%('\n -'.join(miss_pack_msg)))