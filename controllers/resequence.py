from odoo.addons.web.controllers.dataset import DataSet
from odoo.http import request
from odoo import http

# PASSIVE CODE
class ResequenceEnhanced(DataSet):

    @http.route('/web/dataset/resequence', type='json', auth="user")
    def resequence(self, model, ids, field='sequence', offset=0):
        if 'skts' in model:
            m = request.env[model]
            if not m.fields_get([field]):
                return super(ResequenceEnhanced, self).resequence(model, ids, 'sequence', offset)
        return super(ResequenceEnhanced, self).resequence(model, ids, field, offset)
