# -*- coding: utf-8 -*-
from odoo import api, fields, models

OPTIONS_PROCENTAJE_ITEM = [(str(x), x) for x in range(0, 110, 10)]


class ItemRequerimientosSolicitud(models.Model):
    #_inherit = 'ops4g.check_list_event'
    _inherit = 'ops4g.check_list_event'
    _name = 'ops4g.check_list_event'
    # _name='rh.item_requerimiento_solicitud'
    porcentaje = fields.Selection(OPTIONS_PROCENTAJE_ITEM,
                                  string='Porcentaje (%)',
                                  default='0',
                                  required=True)
