# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def _get_name_invoice_pos_report(self):
            """ This method need to be inherit by the localizations if they want to print a custom invoice report instead of
            the default one. For example please review the l10n_ar module """
            self.ensure_one()
            return 'custom_template_sale_invoice.report_invoice_document_sale_pos'

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