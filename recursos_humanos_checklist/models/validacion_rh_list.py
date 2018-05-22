# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ListaRequerimientosSolicitud(models.Model):
    _inherit = 'ops4g.event_model'
    _name = 'rhs4g.requerimientos_solicitud'
    name = fields.Char(string='Nombre del perfil', required=True)
    nivel_academico = fields.Integer(string='Nivel')
    numero_dias_plazo_entrega = fields.Integer(string='Número de días de plazo para entregarlo', required=False)
