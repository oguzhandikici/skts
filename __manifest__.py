{
    "name": "Servis Kayıt ve Takip Sistemi",
    "summary": "",
    "author": "Oguzhan Dikici",

    'category': 'Uncategorized',
    'installable': True,
    'application': True,

    "depends": ['base', 'hr', 'website'],
    "external_dependencies": {'python': []},

    'qweb': [],
    "data": [
        'data/model.xml',
        'data/params.xml',

        'security/security_groups.xml',
        'security/ir.model.access.csv',
        # 'security/access_rules.xml',

        'views/menu_item_view.xml',
        'views/skts_place_view.xml',
        'views/skts_place_term_view.xml',
        'views/skts_place_registration_type_view.xml',
        'views/skts_registration_view.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'skts/static/src/js/website_form.js',
        ]
    }
}
