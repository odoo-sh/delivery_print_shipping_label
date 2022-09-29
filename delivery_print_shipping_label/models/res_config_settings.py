# -*- coding: utf-8 -*-
# Copyright 2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).
from odoo import models,fields

class res_config_setting(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_print_shipment_label = fields.Boolean(string="Auto Print Shipment Label",
                                               config_parameter = "delivery_print_shipping_label.auto_print_shipment_label",
                                               help="Automatically prints the shipment label when DO validated")