# -*- coding: utf-8 -*-

import json
from odoo import api, models, fields, _
from odoo.tools import float_round


class SaleOrderInherit(models.Model):
    _inherit= 'sale.order'
    
    date_order = fields.Datetime(readonly=False,states={}, copy=False)
    date_confirm = fields.Datetime(string='Confirmed Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    rev = fields.Char(string='Rev')
    
    def _prepare_confirmation_values(self):
        return {
            'state': 'sale',
            'date_order': fields.Datetime.now(),
            'date_confirm':fields.Datetime.now()
        }