{
    "name": "Servis Kayıt ve Takip Sistemi",
    "summary": "",
    "author": "Oguzhan Dikici",

    'category': 'Uncategorized',
    'installable': True,
    'application': True,

    "depends": ['base', 'hr'],
    "external_dependencies": {'python': []},

    'qweb': [],
    "data": [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        # 'security/access_rules.xml',

        'views/menu_item_view.xml',
        'views/skts_school_view.xml',
        'views/skts_school_term_view.xml',
        'views/skts_school_registration_type_view.xml',
        'views/skts_person_view.xml',
        'views/skts_registration_view.xml',
        # 'views/skts_registration_school_term_view.xml',
    ],

}
