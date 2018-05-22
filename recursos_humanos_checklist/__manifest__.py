# -*- coding: utf-8 -*-
{
    'name': "RH Check list",

    'summary': """
       RH Check list
        """,

    'description':
        """
               RH Check list
        """,

    'author': "s4g",
    'website': "http://soluciones4g.com",

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': [
        'base',
        'validacion_checklist',
        'hr'
    ],
    'data': [
        'views/datos_requerimientos_solicitud.xml',
        'views/datos_habilidades_rh_solicitud.xml',
        'views/datos_hr_job_inherit.xml',
        'views/datos_hr_applicant_inherit.xml',
        'views/menu.xml'

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
