# -*- coding: utf-8 -*-

import json
from odoo import api, models, fields, _
from odoo.tools import float_round


class ProductInherit(models.Model):
    _inherit= 'product.product'
    
  
    def get_name_report(self):
        if len(self.product_template_attribute_value_ids)>0:
            variant = self.product_template_attribute_value_ids._get_combination_name()
            name = variant and "%s (%s)" % (self.name, variant) or self.name
            return name
        else:
            return self.name  
            
    
    def get_item_nr_report(self):
        if len(self.product_template_attribute_value_ids)>0:
            return self.default_code
        else:
            return self.product_tmpl_id.customer_reference
            