from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class WorkCenter(models.Model):
    _inherit = "mrp.workcenter"

    is_outsource = fields.Boolean(string='Outsource')
    partner_id = fields.Many2one('res.partner', string='Vendor')

    @api.onchange('is_outsource')
    def onchange_is_outsource(self):
        for i in self:
            if not i.is_outsource:
                i.partner_id = False
