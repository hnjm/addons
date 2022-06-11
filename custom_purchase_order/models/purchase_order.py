# -*- coding: utf-8 -*-

import json
from odoo import api, models, fields, _
from odoo.tools import float_round


class PurchaseOrderInherit(models.Model):
    _inherit= 'purchase.order'
    
  
    rev = fields.Char(string='Rev')
  