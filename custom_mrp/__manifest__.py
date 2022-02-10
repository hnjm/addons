# Copyright 2018-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "CUSTOM MRP",
    "version": "15E",
    "category": "MRP MANAGEMENT",
    "license": "AGPL-3",
    "summary": "",
    "author": "Thai Lao",
    "depends": ["base", "mrp_subcontracting", "mrp_workorder"],
    "data": [
        'views/stock_route.xml',
        'views/work_center_view.xml',
        'views/mrp_routing_workcenter_view.xml',
        'views/template_mrp_report_bom_structure.xml'
        ],
    "installable": True,
}
