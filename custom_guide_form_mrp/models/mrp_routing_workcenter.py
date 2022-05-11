# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from datetime import datetime, timedelta
import qrcode
import json
import qrcode
import base64
from io import BytesIO

class MrpRoutingWorkcenterInherit(models.Model):
    _inherit = "mrp.routing.workcenter"
    
    notes = fields.Html(string='Notes')
    
    