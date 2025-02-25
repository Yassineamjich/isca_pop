# -*- coding: utf-8 -*-
{
    'name': "isca_pop",

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
        'security/ir.model.access.csv',
        'views/donation_report.xml',
        'views/baja_item_report.xml',
        'views/category_view.xml',
        'views/move_item_view.xml',
        'views/location_view.xml',
        'views/donate_item.xml',
        'views/cancel_donation.xml',
        'views/donation_view.xml',
        'views/item_view.xml',
        'views/change_stat_wizzard.xml'
        
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}

