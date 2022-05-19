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

    def get_employee_salesperson(self):
        partner = self.env['res.users'].browse(self.user_id.id).partner_id
        return partner.name

    def get_current_week_of_year(self):
        date = datetime.now()
        return date.isocalendar()[1]

    def format_date(self, date):
        if date:
            res = str(date).split('-')
            return '{}-{}-{}'.format(res[2], res[1], res[0])

    def format_currency(self, number):
        currency = "${:,.2f}".format(number)
        return currency


class SaleOderLine(models.Model):
    _inherit = 'sale.order.line'

    def format_currency(self, number):
        currency = "${:,.2f}".format(number)
        return currency

    # def validity_quotation(self):
    #     if self.validity_date and self.date_order:
    #         validity_date = datetime.strptime(str(self.validity_date), '%Y-%m-%d')
    #         date_order = datetime.strptime(str(self.date_order), '%Y-%m-%d %H:%M:%S')
    #         res = validity_date.day - date_order.day
    #         return res



