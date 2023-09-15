odoo.define('skts.website_form', function(require) {
    'use strict';

    if (window.location.pathname === '/registration/form') {
        var ajax = require('web.ajax');

        function setFields(placeField) {
            var selectedPlaceID = placeField.options[placeField.selectedIndex].value;
            var typeField = document.querySelector('[name="type_id"]');
            var placeTermField = document.querySelector('div[name="place_term_ids"]');

            typeField.innerHTML = '';
            placeTermField.innerHTML = '';

            // TERM IDS
            ajax.jsonRpc('/registration/form/skts_search', 'call', {
                model: 'skts.place.term',
                domain: [
                    ['place_id', '=', selectedPlaceID],
                    ['open_to_register', '=', true]
                ],
                fields: ['id', 'name'],
            }).then(function(terms) {
                terms.forEach(function(term) {
                    // Yeni bir div oluşturun
                    console.log(1)
                    console.log(yeniDiv)
                    var yeniDiv = document.createElement('div');
                    yeniDiv.className = 'checkbox col-12';

                    // Yeni bir form-check div oluşturun
                    var yeniFormCheck = document.createElement('div');
                    yeniFormCheck.className = 'form-check';

                    // Yeni bir checkbox oluşturun
                    var yeniCheckbox = document.createElement('input');
                    yeniCheckbox.type = 'checkbox';
                    yeniCheckbox.className = 's_website_form_input form-check-input';
                    yeniCheckbox.id = "customid" + term.id;
                    yeniCheckbox.name = 'place_term_ids';
                    yeniCheckbox.value = term.id;
                    yeniCheckbox.required = '1';
                    yeniCheckbox.setAttribute('data-fill-with', 'undefined');

                    // Yeni bir label oluşturun
                    var yeniLabel = document.createElement('label');
                    yeniLabel.className = 'form-check-label s_website_form_check_label';
                    yeniLabel.setAttribute('for', term.id);
                    yeniLabel.textContent = term.website_display_name; // Bu satırı düzelttim.

                    // Checkbox ve label'ı ilgili div içine ekleyin
                    yeniFormCheck.appendChild(yeniCheckbox);
                    yeniFormCheck.appendChild(yeniLabel);
                    yeniDiv.appendChild(yeniFormCheck);

                    // Yeni oluşturulan div'i "placeTermField" değişkenine ekleyin (hatalı değişken adı düzeltildi).
                    console.log(yeniDiv)
                    placeTermField.appendChild(yeniDiv);
                    console.log(placeTermField)

                });


            });
            // TYPE ID
            ajax.jsonRpc('/registration/form/skts_search', 'call', {
                model: 'skts.place.registration.type',
                domain: [
                    ['place_ids', 'in', [selectedPlaceID]]
                ],
                fields: ['id', 'name'],
            }).then(function(types) {
                types.forEach(function(type) {
                    var option = document.createElement('option');
                    option.value = type.id;
                    option.text = type.name;
                    typeField.appendChild(option);
                });
            });
        }

        function registrationWebsiteForm() {
            var placeField = document.querySelector('[name="place_id"]');
            placeField.innerHTML = '';

            ajax.jsonRpc('/registration/form/skts_search', 'call', {
                model: 'skts.place',
                domain: [
                    ['open_to_register', '=', true]
                ],
                fields: ['id', 'name'],
            }).then(function(places) {
                places.forEach(function(place) {
                    var option = document.createElement('option');
                    option.value = place.id;
                    option.text = place.name;
                    placeField.appendChild(option);
                });
            });

            placeField.addEventListener('change', function() {
                setFields(placeField);
            });
        }

        $(document).ready(function() {
            registrationWebsiteForm();
        });
    }
});