from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'


    worksheet_attachment_ids = fields.Many2many('ir.attachment', string="Upload your file",required=True)
    