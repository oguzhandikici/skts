from odoo.addons.website.controllers.form import WebsiteForm


class RegistrationController(WebsiteForm):

    def extract_data(self, model, values):
        res = super(RegistrationController, self).extract_data(model, values)

        # Website'de oluşturulan forma eklenen alanlar model içerisinde bulunmasa bile "create" metoduna düşürülüyor.
        if model.model == "skts.registration":
            for key in values:
                if key not in res['record']:
                    res['record'][key] = values[key]

        return res
