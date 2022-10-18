from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class MRPRoutingWorkCenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    def _default_time_cycle_manual(self):
        context = self._context
        workcenter_id = context.get('default_workcenter_id') or context.get('active_id')
        if context.get('active_model') == 'mrp.workcenter' and workcenter_id:
            workcenter = self.env['mrp.workcenter'].browse(workcenter_id)
            if workcenter and workcenter.is_outsource:
                return False
        else:
            return 60

    partner_id = fields.Many2one('res.partner', string='Vendor')
    price_cost = fields.Float(string="Cost", digits=(16, 2))
    is_outsource = fields.Boolean(string='Is Outsource', default=False, compute='compute_is_outsource')
    time_cycle_manual = fields.Float(
        'Manual Duration', default=_default_time_cycle_manual,
        help="Time in minutes:"
             "- In manual mode, time used"
             "- In automatic mode, supposed first time when there aren't any work orders yet")

    def compute_is_outsource(self):
        for record in self:
            if record.workcenter_id.is_outsource:
                record.is_outsource = True
            else:
                record.is_outsource = False