{
    'name': 'CRM Lead Days in Work',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Додавання поля "Днів в роботі" до лідів CRM.',
    'depends': ['crm'],
    'data': ['views/crm_lead_views.xml',
             'wizard/client_risk_wizard_views.xml',
             'security/ir.model.access.csv',
             ],
    'installable': True,
    'application': True,
}