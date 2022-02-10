from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class MRPRoutingWorkCenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    partner_id = fields.Many2one('res.partner', string='Vendor')
    price_cost = fields.Float(string="Cost", digits=(16, 2))
    is_outsource = fields.Boolean(string='Is Outsource', default=False, compute='compute_is_outsource')

    def compute_is_outsource(self):
        for record in self:
            if record.workcenter_id.is_outsource:
                record.is_outsource = True
            else:
                record.is_outsource = False