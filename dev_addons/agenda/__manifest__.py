# -*- coding: utf-8 -*-
{
    'name': "agenda",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/security.xml',
        
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/estudiante.xml',
        'views/nivel.xml',
        'views/curso.xml',
        'views/profesor.xml',
        'views/templates.xml',
        'views/cursonivel.xml',
        'views/asistencia.xml',
        
        'views/paralelo.xml',
        'views/materia.xml',
        'views/horario.xml',
        'views/boletin.xml',
        'views/trimestre.xml',
        'views/comunicado.xml',
        'views/users_views.xml',
        'views/pagomensualidad.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
   
}

