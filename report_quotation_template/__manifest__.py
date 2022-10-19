# Copyright 2018-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "REPORT SALE ORDER TEMPLATE",
    "version": "15E",
    "category": "SALE MANAGEMENT",
    "license": "AGPL-3",
    "summary": "",
    "author": "TUONG PHAM",
    "depends": ["sale", "sale_management",'report_template_custom','custom_sale_order'],
    "data": [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'reports/report_sale_order.xml'
    ],
    "installable": True,
}
