# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from datetime import datetime, timedelta
import qrcode
import json
import qrcode
import base64
from io import BytesIO

class AccountMoveInherit(models.Model):
    _inherit = "account.move"
    
    date_print = fields.Date(compute='_compute_date_print' )
    qr_code = fields.Binary('Fanpage FB',compute='_compute_info',store=True)
    wifi =fields.Char('Fanpage FB',compute='_compute_info',store=True)
    passwifi=fields.Char(string='Pass Wifi',compute='_compute_info',store=True)
    

    def _get_name_invoice_pos_report(self):
            """ This method need to be inherit by the localizations if they want to print a custom invoice report instead of
            the default one. For example please review the l10n_ar module """
            self.ensure_one()
            return 'custom_template_sale_invoice.report_invoice_document_sale_pos'
    
    
    def _compute_date_print(self):
        for record in self:
            record.date_print = datetime.now()
            self._compute_info()
            
    @api.depends('date_print')
    def _compute_info(self):
        fanpage = self.env['ir.config_parameter'].sudo().get_param('custom_template_sale_invoice.fanpage_fb')
        wifi = self.env['ir.config_parameter'].sudo().get_param('custom_template_sale_invoice.wifi')
        passwifi = self.env['ir.config_parameter'].sudo().get_param('custom_template_sale_invoice.passwifi')
        for record in self:
            qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
            data=fanpage
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            record.qr_code = base64.b64encode(temp.getvalue())
            record.wifi = wifi
            record.passwifi = passwifi
    
    

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'
    
    def _render_qweb_pdf(self, res_ids=None, data=None):
        # Overridden so that the print > invoices actions raises an error
        # when trying to print a miscellaneous operation instead of an invoice.
        if self.model == 'account.move' and res_ids:
            invoice_reports = (self.env.ref('custom_template_sale_invoice.account_invoices_sale_pos'))
            if self in invoice_reports:
                moves = self.env['account.move'].browse(res_ids)
                if any(not move.is_invoice(include_receipts=True) for move in moves):
                    raise UserError(_("Only invoices could be printed."))

        return super(IrActionsReport, self)._render_qweb_pdf(res_ids=res_ids, data=data)