# Copyright 2018-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "LOCK UOM",
    "version": "15E",
    "category": "ALL",
    "license": "AGPL-3",
    "summary": "",
    "author": "Tran Trang",
    "depends": ["sale", "sale_management",'purchase','account'],
    "data": [
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/purchase_order.xml',

    ],
    "installable": True,
}
