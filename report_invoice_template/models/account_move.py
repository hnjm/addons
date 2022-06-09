from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    
    consignee= fields.Text(string='Consignee:')
    