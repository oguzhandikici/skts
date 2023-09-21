odoo.define('skts.website_form', function(require) {
    'use strict';

    if (window.location.pathname === '/registration/form') {
        var ajax = require('web.ajax');

        async function setFields(placeField) {
            var selectedPlaceID = placeField.options[placeField.selectedIndex].value;
            var typeField = document.querySelector('[name="type_id"]');
            var placeTermField = document.querySelector('div[name="place_term_ids"]');

            typeField.innerHTML = '';
            placeTermField.innerHTML = '';

            // TERM IDS
            await ajax.jsonRpc('/registration/form/skts_search', 'call', {
                model: 'skts.place.term',
                domain: [
                    ['place_id', '=', parseInt(selectedPlaceID)],
                    ['open_to_register', '=', true]
                ],
                fields: ['id', 'website_display_name'],
            }).then(function(terms) {
                terms.forEach(function(term) {
                    // Yeni bir div oluşturun
                    var yeniDiv = document.createElement('div');
                    yeniDiv.className = 'checkbox col-12';

                    // Yeni bir form-check div oluşturun
                    var yeniFormCheck = document.createElement('div');
                    yeniFormCheck.className = 'form-check';

                    // Yeni bir checkbox oluşturun
                    var yeniCheckbox = document.createElement('input');
                    yeniCheckbox.type = 'checkbox';
                    yeniCheckbox.className = 's_website_form_input form-check-input';
                    yeniCheckbox.id = "checkboxid" + term.id;
                    yeniCheckbox.name = 'place_term_ids';
                    yeniCheckbox.value = term.id;
                    yeniCheckbox.required = '1';
                    yeniCheckbox.setAttribute('data-fill-with', 'undefined');
                    if (terms.length === 1) {
                        yeniCheckbox.click();
                    }

                    // Yeni bir label oluşturun
                    var yeniLabel = document.createElement('label');
                    yeniLabel.className = 'form-check-label s_website_form_check_label';
                    yeniLabel.setAttribute('for', "checkboxid" + term.id);
                    yeniLabel.textContent = term.website_display_name; // Bu satırı düzelttim.

                    // Checkbox ve label'ı ilgili div içine ekleyin
                    yeniFormCheck.appendChild(yeniCheckbox);
                    yeniFormCheck.appendChild(yeniLabel);
                    yeniDiv.appendChild(yeniFormCheck);

                    // Yeni oluşturulan div'i "placeTermField" değişkenine ekleyin (hatalı değişken adı düzeltildi).
                    placeTermField.appendChild(yeniDiv);

                });


            });
            // TYPE ID
            await ajax.jsonRpc('/registration/form/skts_search', 'call', {
                model: 'skts.place.registration.type',
                domain: [
                    ['place_id', '=', parseInt(selectedPlaceID)]
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

        async function registrationWebsiteForm() {
            var placeField = document.querySelector('[name="place_id"]');
            placeField.innerHTML = '';

            await ajax.jsonRpc('/registration/form/skts_search', 'call', {
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
            placeField.selectedIndex = 0
            setFields(placeField);

            placeField.addEventListener('change', function() {
                setFields(placeField);
            });
        }

        $(document).ready(function() {
            registrationWebsiteForm();
        });
    }
});