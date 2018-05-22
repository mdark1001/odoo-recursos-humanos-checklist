# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, api, fields
from odoo.tools.safe_eval import safe_eval as eval
from odoo.exceptions import ValidationError, Warning


class EventModel(models.Model):
    _name = 'ops4g.event_model'
    name = fields.Char(string='Nombre del evento', required=True)
    description = fields.Text(string='Descripción')

    nivel_academico = fields.Many2one('ops4g.nivel', string='Nivel académico')

    code = fields.Char(string='Ingrese una clave para el evento', required=True)
    check_list = fields.Many2many(comodel_name='ops4g.check_list_event',
                                  string='Listado de requerimientos'
                                  )
    numero_dias_plazo_entrega = fields.Integer(string='Número de días de plazo para entregarlo', required=True)
    fecha_max_entrega = fields.Date(string='Fecha máxima de entrega')

    _sql_constraints = [
        ('unique_code_and_name', 'UNIQUE(name)', "El nombre ya existe"),
    ]

    @api.onchange('numero_dias_plazo_entrega')
    def _cacular_fecha_entrega_max(self):
        if self.numero_dias_plazo_entrega and self.numero_dias_plazo_entrega > 0:
            fechaActual = datetime.now()  # fecha actual
            dias = timedelta(days=int(self.numero_dias_plazo_entrega))
            self.fecha_max_entrega = fechaActual + dias

    def _validar_lista_items(self, nombre_lista, items_a_validar):
        """
        :param nombre_lista : Object(EventModel)
        :param items_a_validar: Array(Object(CheckListEvent))
        :return: JSON({status:boolean,msg:str,doc:[] })
        """

        validacion = []
        print("----------------Lista a validar " + str(items_a_validar))
        lista = self.env['ops4g.event_model'].search([('id', '=', nombre_lista.id)])
        if lista and len(items_a_validar) > 0:
            lista_doc_requeridos = [x for x in lista.check_list if x.es_requerido == True]
            lista_actual = [x for x in items_a_validar if x.original_entregado or x.copia_entregada]

            for item in lista_doc_requeridos:
                aux_item = [x for x in lista_actual if x.documento_id.id == item.id]

                if not aux_item:
                    validacion.append(item.name)
                else:
                    if (item.requiere_original == True and aux_item[0].original_entregado == False):
                        validacion.append(item.name + " (Original)")
                    elif (item.requiere_copia == True and aux_item[0].copia_entregada == False):
                        validacion.append(item.name + " (Copia)")

            if len(validacion) > 0:
                return {'status': False, 'msg': 'Existen documentos que son requeridos',
                        'doc': u', '.join(validacion).encode('utf-8').strip()}
            elif len(validacion) == 0:
                return {'status': True, 'msg': 'Todo bien'}
        else:
            return {'status': False, 'msg': 'Error al procesar la solicitud'}


    def _execute_source_code(self, item, kwords):
        """
        :param item: Object(ops4g.check_list_event)
        :param kwords: Diccionario con los parametros necesarios para ejecutar el código  almacenado en la db
        :return: True si el codigo almacenado en source_code en el modelo de CheckList
        """
        if (item.source_code and item.source_code != ''):
            kwords['result'] = None
            kwords['temp'] = None
            print(kwords);
            try:
                eval(item.source_code, kwords, mode='exec', nocopy=True);
                print(kwords);
                if kwords['result'] == True:
                    return True
                else:
                    return False
            except:
                raise ValidationError(
                    'Wrong python code defined for rule ' + str(item.name) + ' (' + str(item.source_code) + ').')

        return True


    def evaluar_todos_items(self, lista_itmes, **kwords):
        """
        :param lista_itmes: list(Object(ops4g.check_list_event))
        :param kwords: Extra-Params
        :return: JSON()
        """

        # TODO lo necesario para trabajar
        baselocaldict = {'lista_items': self.env['ops4g.check_list_event'],
                         'aspirantes': self.env['op.admission.register'],
                         'event_model': self.env['ops4g.event_model']
                         }
        if len(kwords) > 0:
            kwords.update(baselocaldict)
        else:
            kwords = baselocaldict

        for item in lista_itmes:
            # print(self._execute_source_code(item, kwords))
            if self._execute_source_code(item, kwords) != True:
                return {
                    'warning': {
                        'title': "Atención",
                        'message': item.message_code_error,
                    },
                }


    def compute_rule_list(self, lista_itmes_check_list, **kwords):
        """
        :param item_check_list: list(Object())
        :param kwords: params as kwords
        :return:
        """
        baselocaldict = {
            'lista_items': self.env['ops4g.check_list_event'],
            'aspirantes': self.env['op.admission.register'],
            'event_model': self.env['ops4g.event_model']
        }
        if len(kwords) > 0:
            kwords.update(baselocaldict)
        else:
            kwords = baselocaldict

        for item in lista_itmes:
            # print(self._execute_source_code(item, kwords))
            if self._execute_source_code(item, kwords) != True:
                return {
                    'warning': {
                        'title': "Atención",
                        'message': item.message_code_error,
                    },
                }


    def compute_rule_item(self, item, **kwords):
        """
        :param item: es un objecto del modelo  ops4g.check_list_event
        :param kwords: es un diccionario que serán los parámetros que podran acceder al codigo almacenado en la base de datos
        :return: JSON({status:Boolean, meg:String})
        """
        baselocaldict = {
            'lista_items': self.env['ops4g.check_list_event'],
            'aspirantes': self.env['op.admission.register'],
            'event_model': self.env['ops4g.event_model']
        }

        if len(kwords) > 0:
            kwords.update(baselocaldict)
        else:
            kwords = baselocaldict
            # print(self._execute_source_code(item, kwords))
            if self._execute_source_code(item, kwords) != True:
                pass
            else:
                pass
