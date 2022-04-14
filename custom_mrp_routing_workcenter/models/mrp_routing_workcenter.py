from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from collections import defaultdict
import base64


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'


    worksheet_attachment_ids = fields.Many2many('ir.attachment', string="Upload your file",required=True)

    @api.model
    def get_attachment(self, id):
        check = self.env['ir.attachment'].browse(id)
        return {
            'res_id': check.res_id,
            'res_model': check.res_model,
            'res_field': check.name
        }
    