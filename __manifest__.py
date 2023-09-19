{
    "name": "Servis Kayıt ve Takip Sistemi",
    "summary": "",
    "author": "Oguzhan Dikici",

    'category': 'Uncategorized',
    'installable': True,
    'application': True,

    "depends": [
        'base', 'hr', 'website',
        'web_notify', 'web_responsive', 'web_group_expand', 'web_refresher', 'web_save_discard_button'
    ],
    "external_dependencies": {'python': []},

    'qweb': [],
    "data": [
        'data/model.xml',
        'data/params.xml',

        'security/security_groups.xml',
        'security/ir.model.access.csv',
        # 'security/access_rules.xml',

        'views/menu_item_view.xml',
        'views/skts_registration_view.xml',
        'views/skts_place_view.xml',
        'views/skts_place_term_view.xml',
        'views/skts_driver_view.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'skts/static/src/js/website_form.js',
        ]
    }
}
