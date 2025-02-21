{
    'name': 'Gestion Reservas',
    'version': '1.0',
    'summary': 'Descripción breve del módulo',
    'author': 'Bugisoft S.A',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/gestion_reservas_views.xml',
        'views/crear_coches_views.xml',
        'views/crear_clientes_views.xml',
        'data/cron_jobs.xml'
    ],
    'installable': True,
    'application': True,
}
