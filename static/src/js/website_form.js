odoo.define('my_module.my_module_website_form', function(require) {
    'use strict';




    function loadPlaceData() {
        if (window.location.pathname === '/registration/form') {
            var rpc = require('web.rpc');
            var placeField = document.querySelector('[name="place_id"]');
            console.log('asdf')

            var res1 = rpc.query({
                model: 'skts.place',
                method: 'search_read',
                args: [[['active', '=', true],['open_to_register', '=', true]],['id', 'name']],
            })
            console.log(res1)
            res1.then(function(places) {
                console.log(places)
                places.forEach(function(place) {
                    console.log(place)
                    var option = document.createElement('option');
                    option.value = place.id;
                    option.text = place.name;
                    placeField.appendChild(option);
                });
            });
        }
    }

    $(document).ready(function() {
        loadPlaceData();
    });
});