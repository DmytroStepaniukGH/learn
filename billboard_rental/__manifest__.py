{
    'name': 'Billboard Rental Management',
    'version': '1.0',
    'summary': 'Manage billboards and their rentals.',
    'depends': ['base', 'web_timeline'],
    'data': [
        'security/ir.model.access.csv',
        'views/billboard_views.xml',
        'views/billboard_rental_views.xml',
        'views/billboard_rental_timeline.xml',
    ],
    'installable': True,
    'application': True,
}