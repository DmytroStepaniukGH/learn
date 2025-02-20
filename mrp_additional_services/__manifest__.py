{
    'name': 'MRP Additional Services',
    'version': '1.0',
    'summary': 'Add additional services to Bills of Materials and Manufacturing Orders.',
    'category': 'Manufacturing',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'application': True,
}
