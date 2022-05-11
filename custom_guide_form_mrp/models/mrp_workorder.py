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
    _inherit = "mrp.workorder"

    def _get_report_base_filename(self):
            self.ensure_one()
            if self.production_id.sale_id:
                return 'Guider Form-%s' % (self.production_id.sale_id.name)
            else:
                return 'Guider Form-%s' % (self.production_id.name)
        
    def _get_name_report_document_guider_form(self):
            """ This method need to be inherit by the localizations if they want to print a custom invoice report instead of
            the default one. For example please review the l10n_ar module """
            self.ensure_one()
            return 'custom_guide_form_mrp.report_document_guider_form'