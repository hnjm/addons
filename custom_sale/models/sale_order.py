from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    status_invoice = fields.Selection([
        ('paid', 'Paid'),
        ('not_paid', 'Not Paid'),
        ('no_invoice', 'Nothing to Invoice')
    ], string='Status of Invoice', compute_sudo='True', compute='_compute_status_invoice')

    def _compute_status_invoice(self):
        for record in self:
            record.status_invoice = 'no_invoice'
            if record.state == 'sale' and record.invoice_ids and (record.invoice_ids.filtered(lambda x: x.state in ['posted'] and x.payment_state == 'paid') and not record.invoice_ids.filtered(lambda x: x.state == 'draft')):
                record.status_invoice = 'paid'
            if record.state == 'sale' and record.invoice_ids and (record.invoice_ids.filtered(lambda x: x.state in ['draft']) or (record.invoice_ids.filtered(lambda x: x.state in ['posted'] and x.payment_state != 'paid') and not record.invoice_ids.filtered(lambda x: x.state == 'draft')) ):
                record.status_invoice = 'not_paid'


    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.sequence.abc') or _('New')
        return super(SaleOrder, self).create(vals)


