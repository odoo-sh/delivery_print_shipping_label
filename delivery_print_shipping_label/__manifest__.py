# Copyright 2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    "name": "Delivery Print Shipping Label",
    "summary": """This module allows to print shipment label after the DO validation""",
    "version": "15.0.1.0.0",
    "category": "Delivery",
    "website": "http://sodexis.com/",
    "author": "Sodexis",
    "license": "OPL-1",
    "installable": True,
    "application": False,
    "depends": [
        'delivery',
        'base_report_to_printer'
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/res_config_setting_views.xml"
    ],
}
