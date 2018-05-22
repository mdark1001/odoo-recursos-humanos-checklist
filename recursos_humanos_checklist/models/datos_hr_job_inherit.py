# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DatosHrJobInherit(models.Model):
    _inherit = 'hr.job'
    _name = 'hr.job'

    perfil = fields.Many2one('rhs4g.requerimientos_solicitud',
                             string='Perfil',
                             required=True)
    habilidades = fields.Many2many(comodel_name = 'ops4g.check_list_event',
                                   string = 'Listado de requerimientos',
                                   related='perfil.check_list',
                                   readonly=True
    )
