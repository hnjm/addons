from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict
import json
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def total_sale_order(self):
        total = json.loads(self.tax_totals_json)
        if total:
            return total['amount_total']

    def validity_quotation(self):
        if self.validity_date and self.date_order:
            validity_date = datetime.strptime(str(self.validity_date), '%Y-%m-%d')
            date_order = datetime.strptime(str(self.date_order), '%Y-%m-%d %H:%M:%S')
            res = validity_date.day - date_order.day
            return res
        return True



