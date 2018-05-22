# -*- coding: utf-8 -*-
{
    'name': "Validación CheckList",

    'summary': """
           CheckList para la validación fácil de "eventos"  
        """,

    'description':
        """
            CheckList para la validación fácil de "eventos"
        """,

    'author': "S4G",
    'website': "",

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': [
        'base'
    ],

    'demo': [],

    'data': [
        'views/check_list_has_partner_action.xml',
        'views/check_list_event.xml',
        'views/check_list_action.xml',
        'views/menu.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'auto_install': False,
}
