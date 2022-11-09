from odoo import api, models, fields, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_id = fields.Many2one('product.product', 'Drawing Nr.', check_company=True,
                                 domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 index=True, required=True, states={'done': [('readonly', True)]})


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_id = fields.Many2one('product.product', 'Drawing Nr.', ondelete="cascade",  check_company=True,
                                 domain="[('type', '!=', 'service'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 index=True)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    product_id = fields.Many2one(
        'product.product', 'Item nr.',
        domain="""[
            ('type', 'in', ['product', 'consu']),
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id)
        ]
        """,
        readonly=True, required=True, check_company=True,
        states={'draft': [('readonly', False)]})


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    product_id = fields.Many2one(string="Drawing Nr", related='production_id.product_id', readonly=True, store=True, check_company=True)
