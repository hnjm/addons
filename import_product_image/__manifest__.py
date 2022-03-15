# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Saritha Sahadevan (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': "Import Product Image",
    'version': '0.1.0.0',
    'summary': """Import Product Image from a URL into Inventory""",
    'description': """Import Product Image from  a URL into Inventory""",
    'author': "Ehio Technologies",
    'company': 'Ehio Technologies',
    'maintainer': 'Ehio Technologies',
    'website': "https://www.ehiotech.com",
    'category': 'Sales',
    'depends': ['sale'],
    'data': ['views/import_product_image_view.xml',
             'security/ir.model.access.csv',],
    'license': 'AGPL-3',
    'images': ['static/description/banner.jpg'],
    'application': False,
    'installable': True,
    'auto_install': False,
}
