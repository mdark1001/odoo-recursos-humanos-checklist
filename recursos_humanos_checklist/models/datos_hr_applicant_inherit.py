# -*- coding: utf-8 -*-
from odoo import api, fields, models

OPTIONS_PROCENTAJE_ITEM = [(str(x), x) for x in range(0, 110, 10)]


class CalifiacionItemRequerimiento(models.Model):
    _name = 'rhs4g.califiacion_item_requerimiento'
    name = fields.Many2one('ops4g.check_list_event', string='Requerimientos', readonly=True)
    cumple_requerimiento = fields.Boolean('¿Cumple?', default=False)
    nivel_cumple = fields.Selection(OPTIONS_PROCENTAJE_ITEM,
                                    string='Porcentaje (%)',
                                    default='0',
                                    required=True)

    hr_applicant_id = fields.Many2one('hr.applicant', string='Aplicación')

    @api.multi
    @api.onchange('cumple_requerimiento')
    def on_change_cumple_cien(self):
        self.nivel_cumple = '100'


class DatosHrJobInherit(models.Model):
    _inherit = 'hr.applicant'
    perfil = fields.Many2one('rhs4g.requerimientos_solicitud',
                             related='job_id.perfil',
                             string='Perfil',
                             readonly=True,
                             required=True)
    habilidades = fields.One2many('rhs4g.califiacion_item_requerimiento', 'hr_applicant_id')

    def generar_items_a_calificar(self):
        habilidades = self.perfil.check_list
        if self.habilidades:
            del_califiacion_habilidad = self.env['rhs4g.califiacion_item_requerimiento'].search(
                [('hr_applicant_id', '=', self.id)])
            if del_califiacion_habilidad.exists():
                del_califiacion_habilidad.unlink()
        if habilidades:
            for x in habilidades:
                # print(x)
                self.env['rhs4g.califiacion_item_requerimiento'].create({
                    'hr_applicant_id': self.id,
                    'name': x.id,

                })
                # return True
