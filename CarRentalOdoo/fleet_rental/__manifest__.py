{
    'name': 'Fleet Rental Management',
    'version': '17.0.1.0.0',
    'summary': """This module will helps you to give the vehicles for Rent.""",
    'depends': ['account', 'fleet', 'mail', 'base', 'bus'],
    'data': [
        'security/fleet_rental_groups.xml',
        'security/fleet_rental_security.xml',
        'security/ir.model.access.csv',
        'data/fleet_rental_data.xml',
        'data/ir_cron_data.xml',
        'views/car_rental_contract_views.xml',
        'views/car_tools_views.xml',
        'views/res_config_settings_views.xml',
        'reports/report_fleet_rental.xml',
        'data/ir_cron_check_assurance.xml',
        'views/cron_popup_views.xml',
        'data/email_template_data.xml',
        'views/res_partner_views.xml',
        'views/fleet_vehicule.xml',
        'views/car_rental_payment_views.xml',
        'views/payment_invoice_template.xml.xml',
        'views/fleet_user_views.xml',
        'views/fleet_rent_report.xml'

        
        
    ],
    'assets': {
        'web.assets_backend': [
            'fleet_rental/static/src/xml/timepicker.xml',
            'fleet_rental/static/src/js/time_widget.js',
            'fleet_rental/static/src/scss/timepicker.scss',



        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
