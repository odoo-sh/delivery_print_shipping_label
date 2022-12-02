# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import _, exceptions, models

import base64
import logging
import os
from tempfile import mkstemp


_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        auto_print_shipment_label = self.env['ir.config_parameter'].sudo().get_param('delivery_print_shipping_label.auto_print_shipment_label')
        if auto_print_shipment_label:
            for picking in self.filtered(lambda x:x.picking_type_code == 'outgoing' and x.carrier_tracking_ref):
                picking.print_shipment_label()
        return res

    def print_shipment_label(self):
        printer_obj = self.env["printing.printer"]
        printer_config_id = self.env['ir.config_parameter'].sudo().get_param('delivery_print_shipping_label.printer_id')
        printer = printer_obj.search([('id','=',int(printer_config_id))])
        if not printer:
            printer = self.env.user.printing_printer_id or printer_obj.get_default()
            if not printer:
                printer = printer_obj.search([],limit=1)
        if printer:
            message_id = self.env["mail.message"].search([('res_id','=',self.id),('model','=',self._name),('body','ilike', '%Shipment created into'), ('body','ilike', F'%{self.carrier_tracking_ref}%')],order='id desc',limit=1)
            for attachment in message_id.attachment_ids:
                behaviour = {
                            'doc_format': attachment.name.split(".")[1],
                            'action': 'server', 
                            'printer': printer, 
                            'tray': False,
                            'title' : attachment.name,
                            'fit-to-page':'True'
                            }
                fd, file_name = mkstemp()
                try:
                    os.write(fd, base64.b64decode(attachment.datas))
                finally:
                    os.close(fd)
                try:
                    printer.print_file(file_name, report=None, **behaviour)
                except Exception:
                    _logger.exception('Error while printing the shipment label')
            if not message_id.attachment_ids:
                if self._context.get('print_via_button',False):
                    raise exceptions.UserError(_("Shipping label(s) not found."))
                else:
                    self.message_post(body=_('Shipping label(s) not found.'),
                              message_type='comment',
                              subtype_xmlid='mail.mt_note')
        else:
            if self._context.get('print_via_button',False):
                action = self.env.ref('base_report_to_printer.printing_server_action')
                msg = _("Please configure the printer")
                raise exceptions.RedirectWarning(msg, action.id, _('Configure Printer'))
            else:
                self.message_post(body=_('No printer configured to print this report.'),
                              message_type='comment',
                              subtype_xmlid='mail.mt_note')
