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
        'security/access_rules.xml',

        'views/menu_item_view.xml',
        'views/test_modulu_users_view.xml',
    ],

}
