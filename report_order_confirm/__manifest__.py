# Copyright 2018-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "REPORT ORDER CONFIRMTATION TEMPLATE",
    "version": "15E",
    "category": "SALE",
    "license": "AGPL-3",
    "summary": "",
    "author": "Tran Trang",
    "depends": ["sale", "sale_management",'report_template_custom','custom_sale_order'],
    "data": [
        'reports/report_order_confirmation.xml',

    ],
    "installable": True,
}
