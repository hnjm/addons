# Copyright 2018-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "REPORT INVOICE TEMPLATE",
    "version": "15E",
    "category": "ACCOUNT",
    "license": "AGPL-3",
    "summary": "",
    "author": "Tran Trang",
    "depends": ["account",'report_template_custom'],
    "data": [
        'reports/report_invoices.xml',
        'reports/report_proforma_invoice.xml',
    ],
    "installable": True,
}
