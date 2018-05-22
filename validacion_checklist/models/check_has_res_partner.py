# -*- coding: utf-8 -*-
from odoo import api, models, fields


class TestSelectionFields(models.Model):
    _name = 'ops4g.check_entregado'

    documento_id = fields.Many2one(
        comodel_name='ops4g.check_list_event',
        string='Seleccione'
    )

    check_list_has_partner_entregado_ids = fields.Many2one(
        comodel_name='ops4g.check_list_has_partner',
        readonly=True
    )
    original_entregado=fields.Boolean()
    copia_entregada=fields.Boolean()

class CheckListHasPartner(models.Model):
    _name = 'ops4g.check_list_has_partner'
    _rec_name =  'name'

    # student_id = fields.Many2one('op.student', 'Estudiante', ondelete="cascade")
    name = fields.Many2one(
        'ops4g.event_model',
        string = "Listado:",
        ondelete="cascade",
        required=True
    )
    lista_completa = fields.Integer(string='Lista completa', compute='get_total_lista', store=True)
    items_list = fields.One2many(
        comodel_name='ops4g.check_entregado',
        inverse_name='check_list_has_partner_entregado_ids',
        ondelete='cascade',
        string='Seleccione'
    )

    @api.onchange('name')
    def get_items_by_list(self):
        # print(self.name.check_list)
        array = [int(x) for x in self.name.check_list]
        self.items_list = []
        if self.name:
            return {'domain': {'items_list': [('id', 'in', array)]}}
        else:
            # remove domain
            return {'domain': {'items_list': []}}
            # self.items_list = self.env['ops4g.check_list_event'].search([('id', 'in', array)])

    @api.depends('items_list')
    @api.onchange('items_list')
    def get_total_lista(self):
        if (self.name):
            # pass
            validacion = self.env['ops4g.event_model']._validar_lista_items(self.name, self.items_list)
            print(validacion)
            # source_code=self.env['ops4g.check_list_event'].evaluar_todos_items(self.items_list)
            total_items_list = [int(x) for x in self.name.check_list]

            # items = self.env['ops4g.check_list_event'].search([('id', 'in', total_items_list)])
            cien_porcieto = len(total_items_list)
            if (cien_porcieto > 0):
                porcentaje = len(self.items_list)
                self.lista_completa = int((porcentaje * 100) / cien_porcieto)
            else:
                self.lista_completa = 0
        else:
            self.lista_completa = 0

    def is_valid_list(self, student_id, list_name_slug):
        # pass
        if student_id and list_name_slug:
            lista_estdiante = self.search([('student_id', '=', student_id), ('name', '=', list_name_slug)])
            if lista_estdiante and lista_estdiante['lista_completa']:
                if (lista_estdiante['lista_completa'] >= 90):
                    return {'status': True,
                            'msg': 'Puede continuar con el proceso'}
                elif (lista_estdiante['lista_completa'] >= 80):
                    return {'status': True,
                            'msg': 'Puede continuar con el proceso'}
            else:
                return {'status': False,
                        'msg': 'Error no se existen registros relacionados'}
        else:
            return {'status': False,
                    'msg': 'Error no se a proporcionado un estudiante valido'}
