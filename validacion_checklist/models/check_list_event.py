# -*- coding: utf-8 -*-
from odoo import models, api, fields


class CheckListEvent(models.Model):
    _name = 'ops4g.check_list_event'

    name = fields.Char(string='Nombre del requerimiento', required=True)

    description = fields.Text(string='Descripción')

    es_requerido = fields.Boolean(string='Marqué si es requerido')

    requiere_original = fields.Boolean(string='Requiere original')

    requiere_copia = fields.Boolean(string='Requiere copia')

    prioridad_lista = fields.Integer(string='Orden en la lista', default=lambda self: 1)

    peso_documento = fields.Float(string='Peso del documento', default=lambda self: 1.0)

    source_code = fields.Text(string='Ingrese en código python la función a evaluar', default='#Este es un comentario')

    message_code_error = fields.Char(string='Ingrese el mensaje de validación', default='Error al validar ')
