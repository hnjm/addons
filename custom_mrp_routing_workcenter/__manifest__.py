# Copyright 2018-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "CUSTOM MRP ROUTING WORKCENTER",
    "version": "15E",
    "category": "Manufacturing/Manufacturing",
    "license": "AGPL-3",
    "summary": "",
    "author": "Tran Trang",
    "depends": ["base", "mrp","web"],
    "data": [
        'views/mrp_routing_workcenter.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_mrp_routing_workcenter/static/src/js/preview_pdf.js'
        ],
        'web.assets_qweb': [
            'custom_mrp_routing_workcenter/static/src/xml/add_preview_pdf.xml'
            
        ],
    },
    "installable": True,
    'application': True,
}
