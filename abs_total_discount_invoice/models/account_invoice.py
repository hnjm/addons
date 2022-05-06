# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api,fields,models,_

class AccountMove(models.Model):
    _inherit = "account.move"

    discount_total = fields.Monetary("Discount Total",compute='total_discount',store=True)
    discount_percent_total = fields.Float("Percentage Discount",compute='total_discount',store=True)
    tax_percent_total = fields.Float("Percentage Tax",compute='total_tax',store=True)
    #Count the total discount
    @api.depends('invoice_line_ids.quantity','invoice_line_ids.price_unit','invoice_line_ids.discount')
    def total_discount(self):
        for invoice in self:
            total_price = 0
            discount_amount = 0
            final_discount_amount = 0
            final_discount_percent_amount=0
            if invoice:  
                for line in invoice.invoice_line_ids:
                    if line:
                        total_price = line.quantity * line.price_unit
                        if total_price:  
                            discount_amount = total_price - line.price_subtotal
                            if discount_amount: 
                                final_discount_amount = final_discount_amount + discount_amount
                        final_discount_percent_amount= final_discount_percent_amount + line.discount
                invoice.update({'discount_total':final_discount_amount,'discount_percent_total':final_discount_percent_amount})
                
    @api.depends('invoice_line_ids.quantity','invoice_line_ids.price_unit','invoice_line_ids.tax_ids')
    def total_tax(self):
        for invoice in self:
            final_discount_percent_tax=0
            if invoice:  
                for line in invoice.invoice_line_ids:
                    if line:
                        final_discount_percent_tax= final_discount_percent_tax + sum(line.tax_ids.mapped('amount'))
                invoice.update({'tax_percent_total':final_discount_percent_tax})

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    
    total_no_dt = fields.Monetary(string='Total', store=True, readonly=True,
        currency_field='currency_id')
    
    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
       
        res = super(AccountMoveLine, self)._get_price_total_and_subtotal_model(price_unit, quantity, discount, currency, product, partner, taxes, move_type)
        subtotal = quantity * price_unit
        res['total_no_dt']=subtotal
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res