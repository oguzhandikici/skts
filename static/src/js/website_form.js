odoo.define('my_module.my_module_website_form', function(require) {
    'use strict';

    function loadPlaceData() {
        if (window.location.pathname === '/registration/form') {
            var ajax = require('web.ajax');
            var placeField = document.querySelector('[name="place_id"]');
            var otherField = document.querySelector('[name="other_field"]');


            ajax.jsonRpc('/registration/form/domain_fields', 'call', {
                model: 'skts.place',
                domain: [['active', '=', true], ['open_to_register', '=', true]],
                fields: ['id', 'name'],
            }).then(function(places) {
                console.log(places);
                places.forEach(function(place) {
                    console.log(place);
                    var option = document.createElement('option');
                    option.value = place.id;
                    option.text = place.name;
                    placeField.appendChild(option);
                });
            });

            placeField.addEventListener('change', function() {
                var selectedPlaceID = placeField.options[placeField.selectedIndex].value;
                parentElement.innerHTML = '';
            });

        }
    }

    $(document).ready(function() {
        loadPlaceData();
    });
});
