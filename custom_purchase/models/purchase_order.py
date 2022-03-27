from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    status_invoice = fields.Selection([
        ('paid', 'Paid'),
        ('not_paid', 'Not Paid'),
        ('no_invoice', 'Nothing to Invoice')
    ], string='Status of Invoice', compute_sudo='True', compute='_compute_status_invoice')

    optional_product = fields.One2many('optional.product', 'purchase_id', string='Optional Product')

    def _compute_status_invoice(self):
        for record in self:
            record.status_invoice = 'no_invoice'
            if record.state == 'purchase' and record.invoice_ids and (record.invoice_ids.filtered(lambda x: x.state in ['posted'] and x.payment_state == 'paid') and not record.invoice_ids.filtered(lambda x: x.state == 'draft')):
                record.status_invoice = 'paid'
            if record.state == 'purchase' and record.invoice_ids and (record.invoice_ids.filtered(lambda x: x.state in ['draft']) or (record.invoice_ids.filtered(lambda x: x.state in ['posted'] and x.payment_state != 'paid') and not record.invoice_ids.filtered(lambda x: x.state == 'draft')) ):
                record.status_invoice = 'not_paid'

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.sequence.abc') or _('New')
        return super(PurchaseOrder, self).create(vals)

    def button_load_optional_product(self):
        for record in self:
            record.optional_product.unlink()
            if record.order_line:
                product = record.order_line.mapped('product_id')
                for pro in product:
                    line = record.order_line.filtered(lambda x: x.product_id.id == pro.id)[0]
                    if line.product_id.optional_product:
                        for opt in line.product_id.optional_product:
                            values = {
                                'purchase_id': record.id,
                                'source_product': line.product_id.id,
                                'optional_product': opt.id
                            }
                            self.env['optional.product'].create(values)


class OptionalProduct(models.Model):
    _name = 'optional.product'

    purchase_id = fields.Many2one('purchase.order')
    source_product = fields.Many2one('product.product', string='Source Product')
    optional_product = fields.Many2one('product.product', string='Optional Product')

    def button_select_optional_product(self):
        for record in self:
            total = sum(i.product_qty for i in record.purchase_id.order_line.filtered(lambda x: x.product_id.id == record.source_product.id))
            product_uom_id = record.purchase_id.order_line.filtered(lambda x: x.product_id.id == record.source_product.id)[0].product_uom
            record.purchase_id.order_line.filtered(lambda x: x.product_id.id == record.source_product.id).unlink()
            values = self.env['purchase.order.line']._prepare_purchase_order_line(
                    record.optional_product,
                    total,
                    product_uom_id,
                    record.purchase_id.company_id,
                    record.purchase_id.partner_id,
                    record.purchase_id,
                )
            self.env['purchase.order.line'].create(values)
            other_product = self.search([
                ('source_product', '=', record.source_product.id)
            ])
            other_product.unlink()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, supplier, po):
        partner = supplier.name
        uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        # _select_seller is used if the supplier have different price depending
        # the quantities ordered.
        seller = product_id.with_company(company_id)._select_seller(
            partner_id=supplier,
            quantity=uom_po_qty,
            date=po.date_order and po.date_order.date(),
            uom_id=product_id.uom_po_id)

        product_taxes = product_id.supplier_taxes_id.filtered(lambda x: x.company_id.id == company_id.id)
        taxes = po.fiscal_position_id.map_tax(product_taxes)

        price_unit = self.env['account.tax']._fix_tax_included_price_company(
            seller.price, product_taxes, taxes, company_id) if seller else 0.0
        if price_unit and seller and po.currency_id and seller.currency_id != po.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, po.currency_id, po.company_id, po.date_order or fields.Date.today())

        product_lang = product_id.with_prefetch().with_context(
            lang=supplier.lang,
            partner_id=supplier.id,
        )
        name = product_lang.with_context(seller_id=seller.id).display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase

        date_planned = self.order_id.date_planned or self._get_date_planned(seller, po=po)

        return {
            'name': name,
            'product_qty': uom_po_qty,
            'product_id': product_id.id,
            'product_uom': product_id.uom_po_id.id,
            'price_unit': price_unit,
            'date_planned': date_planned,
            'taxes_id': [(6, 0, taxes.ids)],
            'order_id': po.id,
        }